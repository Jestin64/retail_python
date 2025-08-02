from pydantic import BaseModel, EmailStr
from models.user import RoleEnum


    
class Userbase(BaseModel):
    username:str
    email: EmailStr
    
class UserCreate(Userbase):
    password: str
    
class UserOut(Userbase):
    id: int
    role: RoleEnum
    
class Config:
    from_attributes = True
   