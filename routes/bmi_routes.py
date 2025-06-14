from fastapi import APIRouter, Depends, Query, HTTPException
from utils.BMI import hitung_bmi_controller
from sqlalchemy.orm import Session
from utils.DB import get_db
from model import bmi as bmi_model
from schema.bmi_schemas import BMICalculateRequest, BMIResponse
from utils.security import get_current_user
from model import user as user_model
from utils.BMI import hitung_bmi_controller


# HAPUS prefix
router = APIRouter(tags=["BMI"])

# TAMBAHKAN /api di path
@router.post("/api/bmi", response_model=BMIResponse)
def hitung_dan_simpan_bmi(
    payload: BMICalculateRequest,  # tanpa id_pengguna
    db: Session = Depends(get_db),
    current_user: user_model.Pengguna = Depends(get_current_user)
):
    result = hitung_bmi_controller(payload.weight, payload.height, payload.unit)

    bmi_record = bmi_model.BMI(
        id_pengguna=current_user.id_pengguna,  # ← ambil dari token login
        berat_badan=payload.weight,
        tinggi_badan=payload.height,
        nilai_bmi=result["bmi"],
        kategori=result["status"].lower()
    )
    db.add(bmi_record)
    db.commit()
    db.refresh(bmi_record)

    return {
        "id_bmi": bmi_record.id_bmi,
        "nilai_bmi": result["bmi"],
        "kategori": result["status"],
        "saran": result["suggestion"]
    }