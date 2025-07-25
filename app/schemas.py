from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActionLogRead(BaseModel):
    id: int
    user_id: int
    action: str
    timestamp: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

class UserRead(BaseModel):
    id: int 
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class LogRead(BaseModel):
    id: int
    user_id: int
    action: str
    timestamp: datetime

    class Config:
        orm_mode = True