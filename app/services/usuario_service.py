from models import Usuario
from werkzeug.security import generate_password_hash


class UsuarioService:
    
    def __init__(self, repository) -> None:
        self.repository = repository
    
    
    def cadastrar(self, dados):
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")
        tipo = dados.get("tipo")
        
        if not nome or not senha or not email or not tipo:
            raise ValueError("Nome, email, senha e tipo são obrigatórios.")
        
        nome = nome.strip()
        email = email.strip().lower()
        senha = senha.strip()
        tipo = tipo.strip()
        usuario = self.repository.buscar_por_email(email)
        
        if usuario:
            raise ValueError("Usuário com mesmo email já cadastrado.")
        
        usuario = Usuario(nome=nome,
                          email=email,
                          senha_hash=generate_password_hash(senha),
                          tipo=tipo)
        
        try:
            self.repository.cadastrar(usuario)
            self.repository.commit()
            return usuario
        
        except Exception:
            self.repository.rollback()
            raise
            
            
        
            
        
        
         