from pydantic import BaseModel
from enum import Enum as PydanticEnum
from fastapi import Query,Path
from datetime import datetime

class TokenCreate(BaseModel):
    token: str
    user_id: str

class TokenRead(TokenCreate):
    token_status: bool
    token_created_at: datetime

class TokenUpdate(BaseModel):
    token: str
    token_status: bool
    