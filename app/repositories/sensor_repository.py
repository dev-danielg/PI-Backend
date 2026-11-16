from app.models import Sensor
from sqlalchemy import select

class SensorRepository:
    def __init__(self, session):
        self.session = session

    def buscar_por_id(self, id):
        query = select(Sensor).where(Sensor.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def buscar_todos(self):
        query = select(Sensor)
        return self.session.execute(query).scalars().all()
    
    def cadastrar(self, sensor):
        self.session.add(sensor)

    def deletar(self, sensor):
        self.session.delete(sensor)

    def atualizar(self, sensor):
        self.session.add(sensor)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
