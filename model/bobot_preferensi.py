from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from utils.DB import Base

class BobotPreferensi(Base):
    __tablename__ = "bobot_preferensi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"), nullable=False)
    id_kriteria = Column(Integer, ForeignKey("kriteria.id_kriteria"), nullable=False)
    bobot = Column(Integer, nullable=False)

    # Relationships
    pengguna = relationship("Pengguna", back_populates="bobot_preferensi")
    kriteria = relationship("Kriteria", back_populates="bobot_preferensi")