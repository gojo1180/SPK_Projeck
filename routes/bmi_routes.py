from fastapi import APIRouter, Query
from utils.BMI import hitung_bmi_controller

# HAPUS prefix
router = APIRouter(
    tags=["BMI"] # Menambahkan tags adalah praktik yang baik
)

# TAMBAHKAN /api di path
@router.get("/api/bmi")
def hitung_bmi(
    weight: float = Query(..., gt=0),
    height: float = Query(..., gt=0),
    unit: str = Query("metric", regex="^(metric|imperial)$")
):
    return hitung_bmi_controller(weight, height, unit)