from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from utils.DB import Base

class Kriteria(Base):
    __tablename__ = "kriteria"

    id_kriteria = Column(Integer, primary_key=True, autoincrement=True)
    nama_kriteria = Column(String(100), nullable=False, unique=True)
    deskripsi = Column(Text)

    # Relationships
    nilai_gizi = relationship("NilaiGizi", back_populates="kriteria")
    bobot_preferensi = relationship("BobotPreferensi", back_populates="kriteria")