from fastapi import APIRouter, Query
from utils.BMI import hitung_bmi_controller



router = APIRouter(
    prefix="/api",
)

@router.get("/bmi")
def hitung_bmi(
    weight: float = Query(..., gt=0),
    height: float = Query(..., gt=0),
    unit: str = Query("metric", regex="^(metric|imperial)$")
):
    return hitung_bmi_controller(weight, height, unit)
