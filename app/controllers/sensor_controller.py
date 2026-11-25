from flask import request


class SensorController:

    def __init__(self, service):
        self.service = service

    def _serializar(self, sensor):
        return {
            "id": sensor.id,
            "nome": sensor.nome,
            "lote_id": sensor.lote_id,
        }

    def cadastrar(self):
        try:
            sensor = self.service.criar(request.get_json() or {})
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Sensor cadastrado com sucesso.",
            "data": self._serializar(sensor),
        }, 201

    def buscar_por_id(self, id):
        try:
            sensor = self.service.buscar_por_id(id)
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        if sensor is None:
            return {"success": False, "message": "Sensor não encontrado."}, 404

        return {"success": True, "data": self._serializar(sensor)}, 200

    def buscar_todos(self):
        try:
            sensores = self.service.buscar_todos()
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "data": [self._serializar(s) for s in sensores],
        }, 200

    def atualizar(self, id):
        try:
            sensor = self.service.atualizar(id, request.get_json() or {})
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Sensor atualizado com sucesso.",
            "data": self._serializar(sensor),
        }, 200

    def deletar(self, id):
        try:
            self.service.deletar(id)
        except ValueError as e:
            return {"success": False, "message": str(e)}, 404
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {"success": True, "message": "Sensor deletado com sucesso."}, 200