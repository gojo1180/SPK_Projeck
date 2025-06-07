from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    nama: str
    password: str
    email: str
    fase_latihan: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id_pengguna: int
    nama: str

    class Config:
        orm_mode = True
