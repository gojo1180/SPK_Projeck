from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from utils.DB import get_db
from model import admin as admin_model
from schema import admin_schemas
from utils import security

router = APIRouter(
    prefix="/admin",
    tags=["Admin Authentication"]
)

@router.post("/create", response_model=admin_schemas.AdminResponseSchema, status_code=status.HTTP_201_CREATED)
def create_admin(admin_data: admin_schemas.AdminCreateSchema, db: Session = Depends(get_db)):
    """
    Membuat admin baru. Sebaiknya hanya digunakan untuk setup awal.
    """
    # Cek apakah email sudah terdaftar
    db_admin = db.query(admin_model.Admin).filter(admin_model.Admin.email == admin_data.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password sebelum disimpan
    hashed_password = security.get_password_hash(admin_data.password)
    
    # Buat objek admin baru dan simpan ke DB
    new_admin = admin_model.Admin(email=admin_data.email, password_hash=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return new_admin


@router.post("/login", response_model=admin_schemas.TokenSchema)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint untuk login admin dan mendapatkan JWT.
    Gunakan form-data dengan key: 'username' (untuk email) dan 'password'.
    """
    # Cari admin berdasarkan email (di form, 'username' dipakai untuk email)
    admin = db.query(admin_model.Admin).filter(admin_model.Admin.email == form_data.username).first()

    # Validasi admin dan password
    if not admin or not security.verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Buat token
    access_token = security.create_access_token(
        data={"sub": admin.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}