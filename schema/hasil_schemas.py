from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HasilCreate(BaseModel):
    id_makanan: int
    skor_total: float
    ranking: int

class HasilWithNamaResponse(BaseModel):
    id_hasil: int
    id_makanan: int
    nama_makanan: str
    gambar: Optional[str] = None  # ← tambahin nih bang
    skor_total: float
    ranking: int
    tanggal_rekomendasi: datetime

    class Config:
        orm_mode = True