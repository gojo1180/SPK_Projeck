from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError

# Impor model dan skema yang diperlukan
from model import admin as admin_model, user as user_model
from schema import admin_schemas
from utils.DB import get_db

load_dotenv()

# --- Konfigurasi Keamanan ---
SECRET_KEY = os.getenv("SECRET_KEY", "your_random_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- 1. Buat DUA skema Oauth2 terpisah ---
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")
user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Konteks untuk hashing password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Fungsi-fungsi Keamanan ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- "Penjaga" untuk Admin dan Pengguna ---
def get_current_admin(token: str = Depends(admin_oauth2_scheme), db: Session = Depends(get_db)) -> admin_model.Admin:
    # 2. Fungsi ini sekarang menggunakan skema admin
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = admin_schemas.TokenDataSchema(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    admin = db.query(admin_model.Admin).filter(admin_model.Admin.email == token_data.email).first()
    if admin is None:
        raise credentials_exception
    return admin

def get_current_user(token: str = Depends(user_oauth2_scheme), db: Session = Depends(get_db)) -> user_model.Pengguna:
    # 3. Fungsi ini sekarang menggunakan skema pengguna
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = db.query(user_model.Pengguna).filter(user_model.Pengguna.id_pengguna == user_id).first()
    if user is None:
        raise credentials_exception
    return user