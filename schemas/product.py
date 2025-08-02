from pydantic import BaseModel
from typing import Optional

# Common fields
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int

# When creating a new product
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]        = None
    description: Optional[str] = None
    price: Optional[float]     = None
    stock: Optional[int]       = None
    category_id: Optional[int] = None

# When sending product in API response
class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
