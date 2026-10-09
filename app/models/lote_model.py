from extension import Base
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Lote(Base):
    __tablename__ = "lote"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fruta: Mapped[str] = mapped_column(String(60), nullable=False)
    status: Mapped[str] = mapped_column(String(60), nullable=False)
    temp_ideal_min: Mapped[float] = mapped_column(Float)
    temp_ideal_max: Mapped[float] = mapped_column(Float)
    umidade_ideal_min: Mapped[float] = mapped_column(Float)
    umidade_ideal_max: Mapped[float] = mapped_column(Float)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
