from pydantic import BaseModel

class KriteriaResponse(BaseModel):
    id_kriteria: int
    nama_kriteria: str
    deskripsi: str | None = None

    class Config:
        from_attributes = True