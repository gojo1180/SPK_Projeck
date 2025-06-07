from pydantic import BaseModel, EmailStr
from typing import Union 

# Skema untuk request body saat login
class AdminLoginSchema(BaseModel):
    email: EmailStr
    password: str

# Skema untuk data di dalam token
class TokenDataSchema(BaseModel):
    email: Union[EmailStr, None] = None 

# Skema untuk response saat login berhasil
class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class AdminCreateSchema(BaseModel):
    email: EmailStr
    password: str

class AdminResponseSchema(BaseModel):
    id_admin: int
    email: EmailStr

    class Config:
        from_attributes = True