from sqlalchemy.orm import Session
from model import bobot_preferensi as bobot_model
from schema.bobot_schemas import BobotCreate
from typing import List

def get_user_preferences(db: Session, user_id: int) -> List[bobot_model.BobotPreferensi]:
    """
    Mengambil semua preferensi bobot milik seorang user dari database.
    """
    # INI LOGIKA YANG BENAR: Langsung query ke database
    return db.query(bobot_model.BobotPreferensi).filter(bobot_model.BobotPreferensi.id_pengguna == user_id).all()

def set_user_preferences(db: Session, user_id: int, preferences_data: BobotCreate) -> List[bobot_model.BobotPreferensi]:
    """
    Mengatur atau memperbarui preferensi bobot user.
    """
    # 1. Hapus semua preferensi lama milik user ini
    db.query(bobot_model.BobotPreferensi).filter(bobot_model.BobotPreferensi.id_pengguna == user_id).delete()
    
    new_preferences = []
    # 2. Masukkan semua preferensi baru dari request
    for pref in preferences_data.preferences:
        new_pref = bobot_model.BobotPreferensi(
            id_pengguna=user_id,
            id_kriteria=pref.id_kriteria,
            bobot=pref.bobot
        )
        db.add(new_pref)
        new_preferences.append(new_pref)
        
    db.commit()
    
    # 3. Refresh objek untuk mendapatkan data terbaru dari DB
    for pref in new_preferences:
        db.refresh(pref)
        
    return new_preferences