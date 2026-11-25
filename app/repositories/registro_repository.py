from app.models import Registro
from sqlalchemy import select


class RegistroRepository:

    def __init__(self, session):
        self.session = session

    def buscar_por_id(self, id):
        query = select(Registro).where(Registro.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def buscar_por_sensor(self, sensor_id):
        query = select(Registro).where(Registro.sensor_id == sensor_id)
        return self.session.execute(query).scalars().all()

    def buscar_todos(self):
        query = select(Registro)
        return self.session.execute(query).scalars().all()

    def cadastrar(self, registro):
        self.session.add(registro)

    def deletar(self, registro):
        self.session.delete(registro)

    def atualizar(self, registro):
        self.session.add(registro)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()