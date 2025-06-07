# app/models/pengguna.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from utils.DB import Base

class Pengguna(Base):
    __tablename__ = "pengguna"

    id_pengguna = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String)
    email = Column(String)
    password = Column(String)

    bmi = relationship("BMI", back_populates="pengguna")
    penilaian = relationship("Penilaian", back_populates="pengguna")
    hasil = relationship("Hasil", back_populates="pengguna")
