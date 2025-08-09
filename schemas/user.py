from pydantic import BaseModel, EmailStr
from models.user import RoleEnum

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Password input when creating user

class UserOut(UserBase):
    id: int
    role: RoleEnum

    class Config:
        orm_mode = True  # Enables compatibility with ORM objects
