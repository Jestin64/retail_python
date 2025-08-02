from sqlalchemy.orm import Session
from models.order import Order, OrderItem
from schemas.order import OrderCreate

def create_order(db: Session, user_id: int, order_in: OrderCreate) -> Order:
    """
    Create a new Order with its items.
    """
    # 1) Build the Order object
    db_order = Order(
        user_id=user_id,
        total=order_in.total,
        status=order_in.status
    )
    # 2) Stage it for insertion
    db.add(db_order)
    # 3) Flush so db_order.id is populated
    db.flush()

    # 4) Loop through each item and create OrderItem rows
    for item in order_in.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order=item.price_at_order
        )
        db.add(db_item)

    # 5) Commit everything in one transaction
    db.commit()
    # 6) Refresh so SQLAlchemy pulls in latest data
    db.refresh(db_order)
    return db_order

def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
    """
    Retrieve all orders placed by this user.
    """
    return db.query(Order).filter(Order.user_id == user_id).all()

def update_order_status(db: Session, order_id: int, new_status: str) -> Order | None:
    """
    Change an order’s status (e.g. pending → shipped).
    """
    db_order = db.query(Order).get(order_id)
    if not db_order:
        return None
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> bool:
    """
    Delete an order and its items.
    """
    db_order = db.query(Order).get(order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True
