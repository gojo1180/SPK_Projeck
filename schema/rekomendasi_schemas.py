from pydantic import BaseModel
from typing import Optional

class RekomendasiResponse(BaseModel):
    id_makanan: int 
    nama: str
    penjelasan: Optional[str] = None
    gambar: Optional[str] = None
    waktu: str
    skor: float

    class Config:
        from_attributes = True