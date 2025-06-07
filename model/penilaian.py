# app/models/penilaian.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from utils.DB import Base

class Penilaian(Base):
    __tablename__ = "penilaian"

    id_penilaian = Column(Integer, primary_key=True, autoincrement=True)
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"))
    id_makanan = Column(Integer, ForeignKey("makanan.id_makanan"))
    id_kriteria = Column(Integer, ForeignKey("kriteria.id_kriteria"))
    nilai = Column(Integer)

    pengguna = relationship("Pengguna", back_populates="penilaian")
    makanan = relationship("Makanan", back_populates="penilaian")
    kriteria = relationship("Kriteria", back_populates="penilaian")
