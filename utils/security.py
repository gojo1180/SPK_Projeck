from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError

from schema import admin_schemas
from model import admin as admin_model
from utils.DB import get_db

load_dotenv()

# --- Konfigurasi Keamanan ---
SECRET_KEY = os.getenv("SECRET_KEY", "your_random_secret_key") #nanti diganti
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> admin_model.Admin:
    """
    Dependency untuk memvalidasi token dan mendapatkan data admin yang sedang login.
    Ini akan menjadi 'gembok' untuk semua endpoint admin.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Validasi payload dengan skema
        token_data = admin_schemas.TokenDataSchema(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    # Cari admin di database
    admin = db.query(admin_model.Admin).filter(admin_model.Admin.email == token_data.email).first()
    if admin is None:
        raise credentials_exception
        
    return admin


# Konteks untuk hashing password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# --- Fungsi-fungsi Keamanan ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Memverifikasi password plain dengan hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Membuat hash dari password."""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Membuat JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt