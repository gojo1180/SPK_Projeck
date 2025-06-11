from pydantic import BaseModel, conint
from typing import List, Optional

# Skema dasar untuk satu preferensi bobot
class BobotBase(BaseModel):
    id_kriteria: int
    bobot: conint(ge=1, le=5) # type: ignore # Angka integer antara 1 dan 5

# Skema untuk membuat/memperbarui satu set preferensi
class BobotCreate(BaseModel):
    preferences: List[BobotBase]

# Skema untuk menampilkan preferensi bobot yang sudah ada
class KriteriaInBobot(BaseModel):
    id_kriteria: int
    nama_kriteria: str

    class Config:
        from_attributes = True

class BobotResponse(BaseModel):
    id_kriteria: int
    bobot: int
    kriteria: KriteriaInBobot # Tampilkan juga nama kriterianya

    class Config:
        from_attributes = True