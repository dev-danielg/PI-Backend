from app.extensions import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from sqlalchemy import String, Integer, Boolean, BigInteger


class Usuario(Base):
    __tablename__ = "usuario"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(180), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] =  mapped_column(String(60), nullable=False)
    mfa_secret: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    mfa_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    mfa_ultimo_passo: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)