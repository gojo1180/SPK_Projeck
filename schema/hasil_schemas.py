from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

# Untuk input simpan hasil SPK
class HasilCreate(BaseModel):
    id_makanan: int
    skor_total: float
    ranking: int
    fase_latihan: str
    waktu_makan: str

# Untuk respon histori flat (tanpa grouping)
class HasilWithNamaResponse(BaseModel):
    id_hasil: int
    id_makanan: int
    nama_makanan: str
    gambar: Optional[str] = None
    skor_total: float
    ranking: int
    tanggal_rekomendasi: datetime

    class Config:
        orm_mode = True

# Untuk item di dalam hasil yang dikelompokkan
class HasilGroupedItem(BaseModel):
    id_hasil: int
    id_makanan: int
    nama_makanan: str
    gambar: Optional[str] = None
    skor_total: float
    ranking: int

# Untuk respon histori grouped
class GroupedHasilResponse(BaseModel):
    tanggal_rekomendasi: date
    fase_latihan: str
    waktu_makan: str
    hasil: List[HasilGroupedItem]
