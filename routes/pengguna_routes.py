from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.DB import get_db
from schema.pengguna_schema import UserCreate, UserLogin, UserResponse
from controller.pengguna_controller import register_user, login_user
from model.user import Pengguna

router = APIRouter(
    prefix="/api",
    tags=["Pengguna"]
)

@router.post("/register", response_model=UserResponse)
def api_register(user: UserCreate, db: Session = Depends(get_db)):
    result = register_user(db, user)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result["data"]  # pastikan controller mengembalikan user di "data"

@router.post("/login", response_model=UserResponse)
def api_login(credentials: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db, credentials)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result["data"]  # controller harus mengembalikan user di "data"

@router.get("/pengguna/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Pengguna).filter(Pengguna.id_pengguna == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")
    return user
