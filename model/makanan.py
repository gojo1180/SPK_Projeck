from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from utils.DB import Base

class Makanan(Base):
    __tablename__ = "makanan"

    id_makanan = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(150), nullable=False, unique=True)
    deskripsi = Column(Text)
    gambar_url = Column(String(255))

    # Relationships
    hasil = relationship("Hasil", back_populates="makanan")
    nilai_gizi = relationship("NilaiGizi", back_populates="makanan", cascade="all, delete-orphan")