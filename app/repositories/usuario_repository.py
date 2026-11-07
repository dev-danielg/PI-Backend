from app.models import Usuario
from sqlalchemy import select


class UsuarioRepository:

    def __init__(self, session):
        self.session = session


    def buscar_por_id(self, id):
        query = select(Usuario).where(Usuario.id == id)
        return self.session.execute(query).scalar_one_or_none()
    
    
    def buscar_por_email(self, email):
        query = select(Usuario).where(Usuario.email == email)
        return self.session.execute(query).scalar_one_or_none()

    
    def buscar_todos(self, nome=None, email=None, tipo=None):
        query = select(Usuario)
        if nome:
            query = query.where(Usuario.nome.ilike(nome))
        if email:
            query = query.where(Usuario.email.ilike(email))
        if tipo:
            query = query.where(Usuario.tipo.ilike(tipo))
            
        return self.session.execute(query).scalars().all()
    
    
    def cadastrar(self, usuario):
        self.session.add(usuario)


    def deletar(self, usuario):
        self.session.delete(usuario)
       
        
    def atualizar(self, usuario):
        self.session.add(usuario)

    
    def commit(self):
        self.session.commit()
    
    
    def rollback(self):
        self.session.rollback()