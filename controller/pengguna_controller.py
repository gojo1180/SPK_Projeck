from sqlalchemy.orm import Session
from model.user import Pengguna
from schema.pengguna_schema import UserCreate, UserLogin, UserUpdate
from utils import security # Impor modul keamanan terpusat kita

def register_user(db: Session, user_data: UserCreate):
    # Cek email
    existing_user = db.query(Pengguna).filter(Pengguna.email == user_data.email).first()
    if existing_user:
        return {"success": False, "message": "Email sudah digunakan."}

    hashed_password = security.get_password_hash(user_data.password)

    new_user = Pengguna(
        nama=user_data.nama,
        email=user_data.email,
        password_hash=hashed_password,
        fase_latihan=user_data.fase_latihan 
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

    if not user or not security.verify_password(credentials.password, user.password_hash):
        return {"success": False, "message": "Email atau password salah."}

    access_token = security.create_access_token(
        data={"sub": user.email, "user_id": user.id_pengguna}
    )

    return {
    "success": True,
    "message": "Login berhasil.",
    "token": {
        "access_token": access_token,
        "token_type": "bearer"
    },
    "user": {
        "id_pengguna": user.id_pengguna,
        "email": user.email,
        "nama": user.nama,
        "fase_latihan": user.fase_latihan
    }
}

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(Pengguna).filter(Pengguna.id_pengguna == user_id).first()
    if not user:
        return {"success": False, "message": "User tidak ditemukan"}

    update_data = user_update.dict(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        hashed_password = security.get_password_hash(update_data["password"])
        update_data["password_hash"] = hashed_password
    
    update_data.pop("password", None)

    # Terapkan perubahan ke objek user
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    
    return {"success": True, "message": "Profil berhasil diperbarui.", "data": user}

 # Asumsikan kamu punya fungsi ini
