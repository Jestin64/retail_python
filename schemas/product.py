from pydantic import BaseModel

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

# When sending product in API response
class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
