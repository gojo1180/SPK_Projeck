from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from utils.DB import get_db
from utils.security import get_current_user
from model.user import Pengguna
from controller import rekomendasi_controller
from schema.rekomendasi_schemas import RekomendasiResponse

router = APIRouter(
    tags=["Rekomendasi"]
)

@router.get("/api/rekomendasi", response_model=List[RekomendasiResponse])
def get_recommendation_api(
    fase_latihan: str = Query(..., enum=["bulking", "cutting", "maintenance"]),
    timing: str = Query(..., enum=["pre_workout", "post_workout"]),
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user)
):
    result = rekomendasi_controller.get_recommendations(db, current_user, timing, fase_latihan)
    if not result["success"]:
        # Gunakan status_code yang sesuai dari controller jika ada, jika tidak 404
        raise HTTPException(status_code=404, detail=result["message"])
    return result["data"]