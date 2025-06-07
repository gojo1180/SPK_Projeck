import enum
from sqlalchemy import Column, Integer, String, Enum, func, DateTime
from sqlalchemy.orm import relationship
from utils.DB import Base

class FaseLatihanEnum(enum.Enum):
    bulking = "bulking"
    cutting = "cutting"
    maintenance = "maintenance"

class Pengguna(Base):
    __tablename__ = "pengguna"

    id_pengguna = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fase_latihan = Column(Enum(FaseLatihanEnum), default=FaseLatihanEnum.maintenance)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    bmi = relationship("BMI", back_populates="pengguna", cascade="all, delete-orphan")
    hasil = relationship("Hasil", back_populates="pengguna", cascade="all, delete-orphan")
    bobot_preferensi = relationship("BobotPreferensi", back_populates="pengguna", cascade="all, delete-orphan")
    nilai_gizi_custom = relationship("NilaiGizi", back_populates="pembuat", cascade="all, delete-orphan")