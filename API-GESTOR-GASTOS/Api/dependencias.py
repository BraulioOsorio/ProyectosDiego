from pydantic import BaseModel

class CateCreate(BaseModel):
    category_name: str
    category_description: str 
    user_status : bool = True

class CateRead(CateCreate):
    category_id :int
