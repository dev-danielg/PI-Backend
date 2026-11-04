from models import Lote
from sqlalchemy import select

class LoteRepository:
    def __init__(self, session):
    
    self.session = session

    def buscar_por_id(self, id):
        query = select(Lote).where(Lote.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def buscar_por_fruta(self, fruta):
        query = select(Lote).where(Lote.fruta == fruta)
        return self.session.execute(query).scalar_one_or_none()

    def buscar_todos(self):
        query = select(Lote)
        return self.session.execute(query).scalarts.all()

    def cadastrar(self, lote):
        self.session.add(lote)

    def deletar(self, usuario):
        self.session.delete(usuario)

    def atualizar(self, usuario):
        self.session.add(usuario)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
