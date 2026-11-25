from datetime import datetime
from app.extensions import Base
from sqlalchemy import String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Registro(Base):
    __tablename__ = "registro"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    umidade_ar: Mapped[float] = mapped_column(Float, nullable=False)
    temperatura_celsius: Mapped[float] = mapped_column(Float, nullable=False)
    umidade_solo: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False)
    tempo_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"), nullable=False)
