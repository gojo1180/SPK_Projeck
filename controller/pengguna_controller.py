from sqlalchemy.orm import Session
from passlib.context import CryptContext
from model.user import Pengguna
from schema.pengguna_schema import UserCreate, UserLogin, UserUpdate
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(db: Session, user: UserCreate):
    existing_user = db.query(Pengguna).filter(Pengguna.email == user.email).first()
    if existing_user:
        return {"success": False, "message": "Email sudah digunakan."}

    hashed_password = pwd_context.hash(user.password)

    new_user = Pengguna(
        nama=user.nama,
        email=user.email,
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "Registrasi berhasil.",
        "data": new_user
    }

def login_user(db: Session, credentials: UserLogin):
    user = db.query(Pengguna).filter(Pengguna.email == credentials.email).first()
    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        return {"success": False, "message": "Email atau password salah."}

    return {
        "success": True,
        "message": "Login berhasil.",
        "data": user
    }

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(Pengguna).filter(Pengguna.id_pengguna == user_id).first()
    if not user:
        return {"success": False, "message": "User tidak ditemukan"}

    data = user_update.dict(exclude_unset=True)  # ambil hanya field yg diisi

    # Hapus password jika ada, agar tidak ikut diperbarui
    data.pop("password", None)

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return {"success": True, "data": user}

