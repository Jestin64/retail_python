from sqlalchemy.orm import Session
from models.order import Order, OrderItem
from models.product import Product
from schemas.order import OrderCreate
from typing import List
from models.order import OrderStatus

def create_order(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    order = Order(user_id=user_id)
    db.add(order)
    db.flush()  # get order.id before adding items

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            raise ValueError(f"Product {item.product_id} unavailable or insufficient stock")

        # Reduce stock
        product.stock -= item.quantity

        db.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        ))

    db.commit()
    db.refresh(order)
    return order

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_all_orders(db: Session) -> List[Order]:
    return db.query(Order).all()

def update_order_status(db: Session, order_id: int, status: OrderStatus) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order
