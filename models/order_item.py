# models/order_item.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id             = Column(Integer, primary_key=True, index=True)
    order_id       = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id     = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity       = Column(Integer, nullable=False)
    price_at_order = Column(Float, nullable=False)

    # Relationships
    order   = relationship("Order", back_populates="items")
    product = relationship("Product")
