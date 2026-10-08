from flask import request


class UsuarioController:
    
    def __init__(self, repository, service):
        self.repository = repository
        self.service = service
        
    def cadastrar(self):
        try:
            usuario = self.service.cadastrar(request.get_json())
        
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        except Exception:
            return {
                "success": False,
                "message": "Erro interno no servidor."
            }, 500
        
        return {
            "success": True,
            "message": "Usuário cadastrado com sucesso.",
            "data": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email
            }
        }, 201
        