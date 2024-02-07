from pydantic import BaseModel,EmailStr
from enum import Enum as PydanticEnum
from datetime import datetime

class UserRole(str,PydanticEnum):
    admin = 'admin'
    user = 'user'

class UserBase(BaseModel):
    full_name: str
    mail: str  #EmailStr

class UserCreate(UserBase):
    passhash:str
    user_role:UserRole
    user_status:bool = True

class UserRead(UserBase):
    user_id :str
    created_at : datetime 
    updated_at : datetime
    user_status : bool
