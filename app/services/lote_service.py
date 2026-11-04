from models import Lote
from repositories import UsuarioRepository

class LoteService:
    
    def __init__(self, repository):
        self.repository = repository

    def criar(self, dados):
        fruta = dados.get("fruta").strip()
        status = dados.get("status").strip()
        temp_ideal_min = dados.get("temp_ideal_min")
        temp_ideal_max = dados.get("temp_ideal_max")
        umidade_ideal_min = dados.get("umidade_ideal_min")
        umidade_ideal_max = dados.get("umidade_ideal_max")
        usuario_id = UsuarioRepository.buscar_por_email(dados.get("usuario_email"))

        if isinstance(temp_ideal_min, float) or isinstance(temp_ideal_max, float):
            temp_ideal_min = float(temp_ideal_min)
            temp_ideal_max = float(temp_ideal_max)
        else:
            raise ValueError("Temperaturas devem ser valores númericos.")

        if isinstance(umidade_ideal_min, float) or isinstance(umidade_ideal_max, float):
            umidade_ideal_min = float(umidade_ideal_min)
            umidade_ideal_max = float(umidade_ideal_max)
        else:
            raise ValueError("Valores de umidade devem ser númericos.")

        lote=Lote(
            fruta=fruta 
            status = status
            temp_ideal_min = temp_ideal_min
            temp_ideal_max = temp_ideal_max
            umidade_ideal_min = umidade_ideal_min
            umidade_ideal_max = umidade_ideal_max)
            usuario_id = usuario_id
        )

        try:
            self.repository.cadastrar(lote)
            self.repository.commit()
            return lote
        except Exception:
            self.rollback()
            raise
