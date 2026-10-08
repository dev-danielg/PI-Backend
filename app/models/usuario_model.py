from extensions import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Usuario(Base):
    __tablename__ = "usuario"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(180), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] =  mapped_column(String(60), nullable=False)
    