from pydantic import BaseModel
from typing import Optional


class MakananCreate(BaseModel):
    nama: str
    deskripsi: Optional[str] = None

    class Config:
        orm_mode = True

class Makanan(BaseModel):
    id_makanan: int
    nama: str
    deskripsi: Optional[str] = None
    #gambar: Optional[str] = None  # Base64 encoded nanti di buks lagi pas production ready

    class Config:
        orm_mode = True

class MakananOut(BaseModel):
    id_makanan: int
    nama: str
    deskripsi: Optional[str]
    gambar: Optional[str]  # base64 string

    class Config:
        orm_mode = True

class MakananSkor(BaseModel):
    id_makanan: int
    nama: str
    skor: float

    class Config:
        orm_mode = True