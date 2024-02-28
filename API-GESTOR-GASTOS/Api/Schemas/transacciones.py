from pydantic import BaseModel,EmailStr
from enum import Enum as PydanticEnum
from datetime import date

class Ttype(str,PydanticEnum):
    revenue = 'revenue'
    expenses = 'expenses'

class TCreate(BaseModel):
    category_id: int 
    amount:float
    t_description:str
    t_type:Ttype

class TRead(TCreate):
    transactions_id:int 
    t_date:date

class TUpdate(BaseModel):
    category_id: int 
    transactions_id:int 
    amount:float
    t_description:str
    t_type:Ttype

