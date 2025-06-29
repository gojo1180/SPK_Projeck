from pydantic import BaseModel, EmailStr
from typing import Optional
from model.user import FaseLatihanEnum 

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    nama: str
    password: str
    email: EmailStr
    #fase_latihan: FaseLatihanEnum 
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    nama: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    fase_latihan: Optional[FaseLatihanEnum] = None 


class UserResponse(BaseModel):
    id_pengguna: int
    nama: str
    email: str
    fase_latihan: Optional[str]

    
    class Config:
        from_attributes = True