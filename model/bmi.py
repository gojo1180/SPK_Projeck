import enum
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
from utils.DB import Base

class KategoriBMIEnum(enum.Enum):
    underweight = "underweight"
    normal = "normal"
    overweight = "overweight"
    obese = "obese"

class BMI(Base):
    __tablename__ = "bmi"

    id_bmi = Column(Integer, primary_key=True, autoincrement=True)
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"), nullable=False)
    berat_badan = Column(Float)
    tinggi_badan = Column(Float)
    nilai_bmi = Column(Float)
    kategori = Column(Enum(KategoriBMIEnum))
    tanggal_dicatat = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    pengguna = relationship("Pengguna", back_populates="bmi")