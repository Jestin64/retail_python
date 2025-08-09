from pydantic import BaseModel
from typing import List
from datetime import datetime
from models.order import OrderStatus

# ---- OrderItem Schemas ----
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True

# ---- Order Schemas ----
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
