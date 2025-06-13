from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from utils.DB import get_db
from schema.pengguna_schema import UserCreate, UserLogin, UserResponse, UserUpdate
from controller.pengguna_controller import register_user, login_user, update_user
from model.user import Pengguna
from schema.admin_schemas import TokenSchema

# HAPUS prefix
router = APIRouter(
    tags=["Pengguna"]
)

# TAMBAHKAN /api di path
@router.post("/api/register", response_model=UserResponse)
def api_register(user: UserCreate, db: Session = Depends(get_db)):
    result = register_user(db, user)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result["data"]

# TAMBAHKAN /api di path
@router.post("/api/login")
def api_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    result = login_user(db, credentials)

    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])

    token = result["token"]
    user = result["user"]

    if not isinstance(token, str):
        raise HTTPException(status_code=500, detail="Token yang dikembalikan bukan string")

    return {
        "access_token": token,
        "user": {
            "id_pengguna": user["id_pengguna"],
            "nama": user["nama"],
            "email": user["email"]
        }
    }

# TAMBAHKAN /api di path
@router.get("/api/pengguna/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Pengguna).filter(Pengguna.id_pengguna == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")
    return user

# TAMBAHKAN /api di path
@router.put("/api/update/{user_id}", response_model=UserResponse)
def api_update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    result = update_user(db, user_id, user_update)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result["data"]