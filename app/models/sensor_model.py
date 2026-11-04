from extension import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Sensor(Base):
  __tablename__ = "sensor"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nome: Mapped[str] = mapped_column(String(120)), nullable=False)
  lote_id: Mapped[int] = mapped_column(ForeignKey("lote.id"), nullable=False)

