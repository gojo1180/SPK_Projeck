from pydantic import BaseModel
from typing import List
from typing import Union, List # <-- 1. Tambahkan Union di sini


# Skema untuk satu item nilai gizi
class NilaiGiziBase(BaseModel):
    id_kriteria: int
    nilai: float

# Skema untuk menampilkan nilai gizi yang sudah ada
class NilaiGizi(NilaiGiziBase):
    id: int

    class Config:
        from_attributes = True

# Skema dasar untuk makanan
class MakananBase(BaseModel):
    nama: str
    deskripsi: Union[str, None] = None 
    gambar_url: Union[str, None] = None


# Skema untuk membuat makanan baru, termasuk nilai gizinya
class MakananCreate(MakananBase):
    nilai_gizi: List[NilaiGiziBase]

# Skema lengkap untuk menampilkan makanan, termasuk ID dan nilai gizinya
class Makanan(MakananBase):
    id_makanan: int
    nilai_gizi: List[NilaiGizi] = []

    class Config:
        from_attributes = True