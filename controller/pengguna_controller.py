from sqlalchemy.orm import Session
from passlib.context import CryptContext
from model.user import Pengguna
from schema.pengguna_schema import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(db: Session, user: UserCreate):
    existing_user = db.query(Pengguna).filter(Pengguna.email == user.email).first()
    if existing_user:
        return {"success": False, "message": "Email sudah digunakan."}

    hashed_password = pwd_context.hash(user.password)

    new_user = Pengguna(
        nama=user.nama,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"success": True, "message": "Registrasi berhasil."}

def login_user(db: Session, credentials: UserLogin):
    user = db.query(Pengguna).filter(Pengguna.email == credentials.email).first()
    if not user or not pwd_context.verify(credentials.password, user.password):
        return {"success": False, "message": "Email atau password salah."}
    
    return {"success": True, "message": "Login berhasil.", "user_id": user.id_pengguna}
