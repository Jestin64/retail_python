# models/order.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from db.session import Base

# import the split‑out class
from .order_item import OrderItem

class Order(Base):
    __tablename__ = "orders"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    total      = Column(Float, nullable=False)
    status     = Column(String, default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user  = relationship("User", back_populates="orders")
    # reference OrderItem by class name, back_populates matches above
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
