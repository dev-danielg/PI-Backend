import json
import os
from datetime import datetime

import thingspeak

from app.models import Registro


class RegistroService:

    def __init__(self, repository, sensor_repository, lote_repository):
        self.repository = repository
        self.sensor_repository = sensor_repository
        self.lote_repository = lote_repository

    # ---------- helpers ----------

    def _converter_float(self, valor, campo):
        try:
            return float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"{campo} deve ser um valor numérico.")

    def _parse_datetime(self, valor):
        """Aceita ISO 8601 (com ou sem 'Z') e retorna datetime naive em UTC."""
        if isinstance(valor, datetime):
            return valor
        try:
            return datetime.fromisoformat(valor.replace("Z", "+00:00")).replace(tzinfo=None)
        except (TypeError, ValueError, AttributeError):
            raise ValueError("tempo_registro deve ser uma data/hora válida (ISO 8601).")

    def _calcular_status(self, umidade_ar, temperatura, umidade_solo, lote):
        """Calcula status com base nas faixas ideais do lote."""
        if lote is None:
            return "desconhecido"

        umidade_ar_ok = lote.umidade_ar_ideal_min <= umidade_ar <= lote.umidade_ar_ideal_max
        temp_ok = lote.temp_ideal_min <= temperatura <= lote.temp_ideal_max
        umidade_solo_ok = lote.umidade_solo_ideal_min <= umidade_solo <= lote.umidade_solo_ideal_max

        return "ok" if (umidade_ar_ok and temp_ok and umidade_solo_ok) else "alerta"

    def _validar_sensor(self, sensor_id):
        try:
            sensor_id = int(sensor_id)
        except (TypeError, ValueError):
            raise ValueError("sensor_id deve ser um número inteiro.")

        sensor = self.sensor_repository.buscar_por_id(sensor_id)
        if sensor is None:
            raise ValueError("Sensor não encontrado.")
        return sensor

    # ---------- mapeamento ThingSpeak (recebido via POST) ----------

    def criar_a_partir_thingspeak(self, dados_thingspeak, sensor_id):
        """
        Recebe o dict retornado por channel.get() do ThingSpeak
        e mapeia para um Registro.

        Estrutura esperada:
        {
            "feeds": [
                {
                    "created_at": "2026-11-06T14:30:00Z",
                    "entry_id": 123,
                    "field1": "65.5",   # umidade
                    "field2": "22.3",    # temperatura_celsius
                    "field3": "60.2"    # umidade_solo
                }
            ]
        }
        """
        feeds = dados_thingspeak.get("feeds")
        if not feeds:
            raise ValueError("Nenhum feed retornado pelo ThingSpeak.")

        feed = feeds[0]

        field_umidade_ar = os.getenv("THINGSPEAK_FIELD_UMIDADE_AR", "field1")
        field_temperatura = os.getenv("THINGSPEAK_FIELD_TEMPERATURA", "field2")
        field_umidade_solo = os.getenv("THINGSPEAK_FIELD_UMIDADE_SOLo", "field3")

        umidade_ar_raw = feed.get(field_umidade_ar)
        temperatura_raw = feed.get(field_temperatura)
        umidade_solo_raw = feed.get(field_umidade_solo)
        created_at = feed.get("created_at")

        if umidade_ar_raw is None:
            raise ValueError(f"{field_umidade_ar} (umidade) ausente no feed do ThingSpeak.")
        if temperatura_raw is None:
            raise ValueError(f"{field_temperatura} (temperatura) ausente no feed do ThingSpeak.")
        if umidade_solo_raw is None:
            raise ValueError(f"{field_umidade_solo} (umidade) ausente no feed do ThingSpeak.")

        umidade_ar = self._converter_float(umidade_ar_raw, "umidade_ar")
        temperatura = self._converter_float(temperatura_raw, "temperatura_celsius")
        umidade_solo = self._converter_float(umidade_solo_raw, "umidade_solo")
        tempo_registro = self._parse_datetime(created_at)

        sensor = self._validar_sensor(sensor_id)

        lote = self.lote_repository.buscar_por_id(sensor.lote_id)
        status = self._calcular_status(umidade_ar, temperatura, umidade_solo, lote)

        registro = Registro(
            umidade_ar=umidade_ar,
            temperatura_celsius=temperatura,
            umidade_solo=umidade_solo,
            status=status,
            tempo_registro=tempo_registro,
            sensor_id=sensor.id
        )

        try:
            self.repository.cadastrar(registro)
            self.repository.commit()
            return registro
        except Exception:
            self.repository.rollback()
            raise

    # ---------- integração ativa: backend busca no ThingSpeak ----------

    def sincronizar_do_thingspeak(self, sensor_id):
        """
        O backend consulta o ThingSpeak diretamente e persiste o último registro.
        Não depende de script externo nem de body no POST.
        """
        channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
        read_key = os.getenv("THINGSPEAK_READ_KEY")

        if not channel_id or not read_key:
            raise ValueError(
                "THINGSPEAK_CHANNEL_ID e THINGSPEAK_READ_KEY precisam estar no .env."
            )

        try:
            channel = thingspeak.Channel(id=int(channel_id), api_key=read_key)
            response = channel.get({"result": 1})
        except Exception as e:
            raise ValueError(f"Falha ao consultar o ThingSpeak: {e}")

        try:
            dados = json.loads(response)
        except (TypeError, ValueError):
            raise ValueError("Resposta do ThingSpeak não é um JSON válido.")

        return self.criar_a_partir_thingspeak(dados, sensor_id)

    # ---------- CRUD padrão ----------

    def criar(self, dados):
        """Criação manual (sem ThingSpeak), útil para testes ou fallback."""
        umidade_ar = self._converter_float(dados.get("umidade_ar"), "umidade_ar")
        temperatura = self._converter_float(dados.get("temperatura_celsius"), "temperatura_celsius")
        umidade_solo = self._converter_float(dados.get("umidade_solo"), "umidade_solo")

        status = (dados.get("status") or "").strip()
        if not status:
            raise ValueError("status é obrigatório na criação manual.")

        tempo_registro = self._parse_datetime(dados.get("tempo_registro"))
        sensor = self._validar_sensor(dados.get("sensor_id"))

        registro = Registro(
            umidade_ar=umidade_ar,
            temperatura_celsius=temperatura,
            umidade_solo=umidade_solo,
            status=status,
            tempo_registro=tempo_registro,
            sensor_id=sensor.id
        )

        try:
            self.repository.cadastrar(registro)
            self.repository.commit()
            return registro
        except Exception:
            self.repository.rollback()
            raise

    def buscar_por_id(self, id):
        return self.repository.buscar_por_id(id)

    def buscar_por_sensor(self, sensor_id):
        return self.repository.buscar_por_sensor(sensor_id)

    def buscar_todos(self):
        return self.repository.buscar_todos()

    def atualizar(self, id, dados):
        registro = self.repository.buscar_por_id(id)
        if registro is None:
            raise ValueError("Registro não encontrado.")

        if "umidade_ar" in dados:
            registro.umidade_ar = self._converter_float(dados["umidade_ar"], "umidade_ar")
        if "temperatura_celsius" in dados:
            registro.temperatura_celsius = self._converter_float(
                dados["temperatura_celsius"], "temperatura_celsius"
            )
        if "umidade_solo" in dados:
            registro.umidade_solo = self._converter_float(dados["umidade_solo"], "umidade_solo")
        if "status" in dados:
            status = (dados.get("status") or "").strip()
            if not status:
                raise ValueError("status não pode ser vazio.")
            registro.status = status
        if "tempo_registro" in dados:
            registro.tempo_registro = self._parse_datetime(dados["tempo_registro"])
        if "sensor_id" in dados:
            sensor = self._validar_sensor(dados["sensor_id"])
            registro.sensor_id = sensor.id

        try:
            self.repository.atualizar(registro)
            self.repository.commit()
            return registro
        except Exception:
            self.repository.rollback()
            raise

    def deletar(self, id):
        registro = self.repository.buscar_por_id(id)
        if registro is None:
            raise ValueError("Registro não encontrado.")

        try:
            self.repository.deletar(registro)
            self.repository.commit()
            return True
        except Exception:
            self.repository.rollback()
            raise
