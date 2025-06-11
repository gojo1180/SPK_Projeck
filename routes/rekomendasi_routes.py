from fastapi import APIRouter, Depends, Query, HTTPException 
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel 

from utils.DB import get_db
from utils.security import get_current_user
from model.user import Pengguna
from controller import rekomendasi_controller
from schema.makanan_schemas import Makanan as MakananSchema # Impor skema Makanan

router = APIRouter(
    prefix="/api",
    tags=["Rekomendasi"]
)

# Definisikan skema untuk respons di sini
class RekomendasiResponse(BaseModel):
    makanan: MakananSchema # Gunakan skema Makanan yang sudah diimpor
    skor: float

    class Config:
        from_attributes = True


@router.get("/rekomendasi", response_model=List[RekomendasiResponse])
def get_recommendation_api(
    timing: str = Query(..., enum=["pre_workout", "post_workout"]),
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user)
):
    result = rekomendasi_controller.get_recommendations(db, current_user, timing)
    if not result["success"]:
        # Sekarang HTTPException sudah dikenali
        raise HTTPException(status_code=404, detail=result["message"])
    return result["data"]