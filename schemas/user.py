from pydantic import BaseModel, EmailStr
from enum import Enum


class RoleEnum(str,Enum):
    customer = "customer"
    admin = "admin"
    
class Userbase(BaseModel):
    username:str
    email: EmailStr
    
class UserCreate(Userbase):
    password: str
    
class UserOut(Userbase):
    id: int
    role: RoleEnum
    
    class Config:
        orm_mode =True
   