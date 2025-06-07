# app/models/bmi.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.DB import Base

class BMI(Base):
    __tablename__ = "bmi"

    id_bmi = Column(Integer, primary_key=True, autoincrement=True)
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"))
    berat_badan = Column(Float)
    tinggi_badan = Column(Float)
    nilai_bmi = Column(Float)
    kategori = Column(String)

    pengguna = relationship("Pengguna", back_populates="bmi")
