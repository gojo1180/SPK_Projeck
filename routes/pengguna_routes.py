from fastapi import APIRouter, Depends, HTTPException, Request
# 1. Impor komponen yang diperlukan
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session

from utils.DB import get_db
from schema.pengguna_schema import UserCreate, UserLogin, UserResponse, UserUpdate
from controller.pengguna_controller import register_user, login_user, update_user
from model.user import Pengguna
from schema.admin_schemas import TokenSchema 

router = APIRouter(
    prefix="/api",
    tags=["Pengguna"]
)

@router.post("/register", response_model=UserResponse)
def api_register(user: UserCreate, db: Session = Depends(get_db)):
    result = register_user(db, user)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result["data"]

# --- UBAH FUNGSI DI BAWAH INI ---
@router.post("/login", response_model=TokenSchema)
def api_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 2. Ubah parameter dari `credentials: UserLogin` menjadi `form_data: OAuth2PasswordRequestForm`
    
    # Buat objek UserLogin secara manual untuk dikirim ke controller
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    
    result = login_user(db, credentials) # Kirim ke controller
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result["token"]
# --- PERUBAHAN SELESAI ---

@router.get("/pengguna/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Pengguna).filter(Pengguna.id_pengguna == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")
    return user

@router.put("/update/{user_id}", response_model=UserResponse)
def api_update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    result = update_user(db, user_id, user_update)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result["data"]
