from app.models import Sensor


class SensorService:

    def __init__(self, repository, lote_repository):
        self.repository = repository
        self.lote_repository = lote_repository

    def criar(self, dados):
        nome = (dados.get("nome") or "").strip()
        lote_id = dados.get("lote_id")

        if not nome:
            raise ValueError("Nome do sensor é obrigatório.")

        if lote_id is None:
            raise ValueError("lote_id é obrigatório.")

        try:
            lote_id = int(lote_id)
        except (TypeError, ValueError):
            raise ValueError("lote_id deve ser um número inteiro.")

        lote = self.lote_repository.buscar_por_id(lote_id)
        if lote is None:
            raise ValueError("Lote não encontrado.")

        sensor = Sensor(
            nome=nome,
            lote_id=lote_id
        )

        try:
            self.repository.cadastrar(sensor)
            self.repository.commit()
            return sensor
        except Exception:
            self.repository.rollback()
            raise

    def buscar_por_id(self, id):
        return self.repository.buscar_por_id(id)

    def buscar_todos(self):
        return self.repository.buscar_todos()

    def atualizar(self, id, dados):
        sensor = self.repository.buscar_por_id(id)
        if sensor is None:
            raise ValueError("Sensor não encontrado.")

        if "nome" in dados:
            nome = (dados.get("nome") or "").strip()
            if not nome:
                raise ValueError("Nome do sensor não pode ser vazio.")
            sensor.nome = nome

        if "lote_id" in dados:
            try:
                lote_id = int(dados.get("lote_id"))
            except (TypeError, ValueError):
                raise ValueError("lote_id deve ser um número inteiro.")
            if self.lote_repository.buscar_por_id(lote_id) is None:
                raise ValueError("Lote não encontrado.")
            sensor.lote_id = lote_id

        try:
            self.repository.atualizar(sensor)
            self.repository.commit()
            return sensor
        except Exception:
            self.repository.rollback()
            raise

    def deletar(self, id):
        sensor = self.repository.buscar_por_id(id)
        if sensor is None:
            raise ValueError("Sensor não encontrado.")

        try:
            self.repository.deletar(sensor)
            self.repository.commit()
            return True
        except Exception:
            self.repository.rollback()
            raise