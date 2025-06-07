from sqlalchemy import Column, Integer, String, Text, LargeBinary
from utils.DB import Base
from sqlalchemy.orm import relationship

class Makanan(Base):
    __tablename__ = "makanan"

    id_makanan = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String)
    gambar = Column(LargeBinary)  # untuk menyimpan file binary (BYTEA)
    deskripsi = Column(Text)

    penilaian = relationship("Penilaian", back_populates="makanan")
    hasil = relationship("Hasil", back_populates="makanan")
