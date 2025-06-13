from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from utils.DB import get_db
from utils.security import get_current_user
from model.user import Pengguna
from controller import preferensi_controller

# Skema yang dibutuhkan dari bobot_schemas
from schema.bobot_schemas import BobotResponse, BobotCreate, BobotBase 

router = APIRouter(
    tags=["Preferensi Pengguna"]
)

# Endpoint GET untuk mengambil preferensi
@router.get("/api/users/me/preferences", response_model=List[BobotResponse])
def get_user_preferences_api(
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user)
):
    # PERBAIKAN: Panggil nama fungsi yang benar dari controller
    return preferensi_controller.get_user_preferences(db, current_user.id_pengguna)

# Endpoint PUT untuk memperbarui preferensi
@router.put("/api/users/me/preferences", response_model=List[BobotResponse])
def update_user_preferences_api(
    preferences_data: BobotCreate, # Menggunakan skema BobotCreate untuk menerima data
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user)
):
    # PERBAIKAN: Panggil nama fungsi yang benar dari controller
    return preferensi_controller.set_user_preferences(db, current_user.id_pengguna, preferences_data)