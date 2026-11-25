from flask import request


class LoteController:

    def __init__(self, service):
        self.service = service

    def _serializar(self, lote):
        return {
            "id": lote.id,
            "fruta": lote.fruta,
            "status": lote.status,
            "temp_ideal_min": lote.temp_ideal_min,
            "temp_ideal_max": lote.temp_ideal_max,
            "umidade_ar_ideal_min": lote.umidade_ar_ideal_min,
            "umidade_ar_ideal_max": lote.umidade_ar_ideal_max,
            "umidade_solo_ideal_min": lote.umidade_solo_ideal_min,
            "umidade_solo_ideal_max": lote.umidade_solo_ideal_max,
            "usuario_id": lote.usuario_id,
        }

    def cadastrar(self):
        try:
            lote = self.service.criar(request.get_json() or {})
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Lote cadastrado com sucesso.",
            "data": self._serializar(lote),
        }, 201

    def buscar_por_id(self, id):
        try:
            lote = self.service.buscar_por_id(id)
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        if lote is None:
            return {"success": False, "message": "Lote não encontrado."}, 404

        return {"success": True, "data": self._serializar(lote)}, 200

    def buscar_todos(self):
        try:
            lotes = self.service.buscar_todos()
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "data": [self._serializar(l) for l in lotes],
        }, 200

    def atualizar(self, id):
        try:
            lote = self.service.atualizar(id, request.get_json() or {})
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Lote atualizado com sucesso.",
            "data": self._serializar(lote),
        }, 200

    def deletar(self, id):
        try:
            self.service.deletar(id)
        except ValueError as e:
            return {"success": False, "message": str(e)}, 404
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {"success": True, "message": "Lote deletado com sucesso."}, 200