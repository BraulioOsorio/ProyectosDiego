from pydantic import BaseModel

class CateCreate(BaseModel):
    category_name: str
    category_description: str 

class CateRead(CateCreate):
    category_id :int

class CateUpdate(CateCreate):
    category_id : int
    category_status : bool
