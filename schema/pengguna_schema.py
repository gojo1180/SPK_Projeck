from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    nama: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    nama: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    fase_latihan: Optional[str] = None

class UserResponse(UserBase):
    id_pengguna: int
    nama: str
    fase_latihan: Optional[str] = None  # ditambahkan untuk response user
    
    class Config:
        orm_mode = True

