# app/models/kriteria.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from utils.DB import Base

class Kriteria(Base):
    __tablename__ = "kriteria"

    id_kriteria = Column(Integer, primary_key=True, autoincrement=True)
    nama_kriteria = Column(String)
    bobot = Column(Integer)
    deskripsi = Column(Text)

    penilaian = relationship("Penilaian", back_populates="kriteria")
