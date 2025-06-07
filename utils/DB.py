from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

# Tentukan path .env dari root project (1 folder di atas utils)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    sys.exit(" DATABASE_URL tidak ditemukan! Pastikan .env ada di root project dan variabelnya benar.")

# Untuk Supabase wajib pakai sslmode=require
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency FastAPI untuk db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
