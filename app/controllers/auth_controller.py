from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity


class AuthController:

    def __init__(self, service):
        self.service = service

    def _emitir_token(self, usuario):
        return create_access_token(
            identity=str(usuario.id),
            additional_claims={"role": usuario.tipo},
        )

    def login(self):
        try:
            usuario = self.service.login(request.get_json() or {})

        except ValueError as e:
            return {"success": False, "message": str(e)}, 401

        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        if usuario.mfa_ativo:
            return {
                "success": True,
                "message": "Informe o código do aplicativo autenticador.",
                "data": {
                    "mfa_required": True,
                    "mfa_token": self.service.gerar_mfa_token(usuario),
                },
            }, 200

        return {
            "success": True,
            "message": "Usuário logado com sucesso.",
            "data": {
                "usuario": usuario.nome,
                "email": usuario.email,
                "access_token": self._emitir_token(usuario),
            },
        }, 200


    def verificar_mfa(self):
        try:
            usuario = self.service.verificar_login_mfa(request.get_json() or {})

        except ValueError as e:
            return {"success": False, "message": str(e)}, 401

        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Usuário logado com sucesso.",
            "data": {
                "usuario": usuario.nome,
                "email": usuario.email,
                "access_token": self._emitir_token(usuario),
            },
        }, 200


    def iniciar_mfa(self):
        try:
            dados = self.service.iniciar_mfa(get_jwt_identity())

        except ValueError as e:
            return {"success": False, "message": str(e)}, 400

        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Cadastre o segredo no aplicativo e confirme em /api/auth/mfa/ativar.",
            "data": dados,
        }, 200


    def ativar_mfa(self):
        try:
            self.service.ativar_mfa(get_jwt_identity(), request.get_json() or {})

        except ValueError as e:
            return {"success": False, "message": str(e)}, 400

        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {"success": True, "message": "MFA ativado com sucesso."}, 200


    def desativar_mfa(self):
        try:
            self.service.desativar_mfa(get_jwt_identity(), request.get_json() or {})

        except ValueError as e:
            return {"success": False, "message": str(e)}, 400

        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {"success": True, "message": "MFA desativado com sucesso."}, 200  