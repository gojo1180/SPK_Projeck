from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from utils.DB import get_db
from utils.security import get_current_user
from model.user import Pengguna
from schema import bobot_schemas
from controller import preferensi_controller

router = APIRouter(
    prefix="/api/users/me/preferences", # Endpoint di bawah profil user
    tags=["Preferensi Pengguna"],
    dependencies=[Depends(get_current_user)] # Lindungi semua endpoint di sini
)

@router.get("/", response_model=List[bobot_schemas.BobotResponse])
def read_user_preferences(
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user)
):
    """Mendapatkan daftar preferensi bobot kustom milik pengguna yang sedang login."""
    return preferensi_controller.get_user_preferences(db, user_id=current_user.id_pengguna)

@router.put("/", response_model=List[bobot_schemas.BobotResponse])
def update_user_preferences(
    preferences_data: bobot_schemas.BobotCreate,
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user)
):
    """
    Mengatur (membuat atau menimpa) preferensi bobot kustom untuk pengguna
    yang sedang login.
    """
    return preferensi_controller.set_user_preferences(db, user_id=current_user.id_pengguna, preferences_data=preferences_data)