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
        
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 500
        
        return {
            "success": True,
            "message": "Usuário cadastrado com sucesso.",
            "data": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo
            }
        }, 201
        
    
    def buscar_todos(self):
        nome = request.args.get("nome")
        email = request.args.get("email")
        tipo = request.args.get("tipo")
        
        try:
            usuarios = self.service.buscar_todos(nome, email, tipo)

        except LookupError as e:
            return {
                "success": False,
                "message": str(e)
            }, 404
            
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 500
            
        return {
            "success": True,
            "message": "Usuários buscados com sucesso.",
            "data": [{
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo
            } for usuario in usuarios]
        }, 200
        
    
    def deletar(self, id):
        try:
            usuario = self.service.deletar(id)
        
        except LookupError as e:
            return {
                "success": False,
                "message": str(e)
            }, 404
        
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 500
        
        return {
            "success": True,
            "message": "Usuário deletado com sucesso.",
            "data": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo
            }
        }, 200
        
    
    def atualizar(self, id):
        try: 
            usuario = self.service.atualizar(id)
        
        except LookupError as e:
            return {
                "success": False,
                "message": str(e)
            }, 404
        
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 500
            
        return {
            "success": True,
            "message": "Usuário atualizado com sucesso.",
            "data": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo
            }
        }, 200
        