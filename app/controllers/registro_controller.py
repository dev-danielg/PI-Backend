from flask import request


class RegistroController:

    def __init__(self, service):
        self.service = service

    def _serializar(self, registro):
        return {
            "id": registro.id,
            "umidade_ar": registro.umidade_ar,
            "umidade_solo": registro.umidade_solo,
            "temperatura_celsius": registro.temperatura_celsius,
            "status": registro.status,
            "tempo_registro": registro.tempo_registro.isoformat()
                if registro.tempo_registro else None,
            "sensor_id": registro.sensor_id,
        }

    def cadastrar(self):
        try:
            registro = self.service.criar(request.get_json() or {})
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Registro cadastrado com sucesso.",
            "data": self._serializar(registro),
        }, 201

    def cadastrar_thingspeak(self, sensor_id):
        """
        Recebe o JSON cru do ThingSpeak no body:
        { "feeds": [ { "created_at": "...", "field1": "...", "field2": "..." } ] }
        """
        try:
            dados = request.get_json() or {}
            registro = self.service.criar_a_partir_thingspeak(dados, sensor_id)
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Registro importado do ThingSpeak com sucesso.",
            "data": self._serializar(registro),
        }, 201
        
    def sincronizar_thingspeak(self, sensor_id):
        try:
            registro = self.service.sincronizar_do_thingspeak(sensor_id)
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Registro sincronizado do ThingSpeak com sucesso.",
            "data": self._serializar(registro),
        }, 201
        
    def buscar_por_id(self, id):
        try:
            registro = self.service.buscar_por_id(id)
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        if registro is None:
            return {"success": False, "message": "Registro não encontrado."}, 404

        return {"success": True, "data": self._serializar(registro)}, 200

    def buscar_por_sensor(self, sensor_id):
        try:
            registros = self.service.buscar_por_sensor(sensor_id)
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "data": [self._serializar(r) for r in registros],
        }, 200

    def buscar_todos(self):
        try:
            registros = self.service.buscar_todos()
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "data": [self._serializar(r) for r in registros],
        }, 200

    def atualizar(self, id):
        try:
            registro = self.service.atualizar(id, request.get_json() or {})
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {
            "success": True,
            "message": "Registro atualizado com sucesso.",
            "data": self._serializar(registro),
        }, 200

    def deletar(self, id):
        try:
            self.service.deletar(id)
        except ValueError as e:
            return {"success": False, "message": str(e)}, 404
        except Exception:
            return {"success": False, "message": "Erro interno no servidor."}, 500

        return {"success": True, "message": "Registro deletado com sucesso."}, 200