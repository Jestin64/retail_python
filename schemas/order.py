from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_order: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    total: float
    status: str = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
