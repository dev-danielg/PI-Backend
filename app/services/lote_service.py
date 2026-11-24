from app.models import Lote


class LoteService:

    def __init__(self, repository, usuario_repository):
        self.repository = repository
        self.usuario_repository = usuario_repository

    def _converter_float(self, valor, campo):
        try:
            return float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"{campo} deve ser um valor numérico.")

    def _validar_faixas(self, temp_min, temp_max, umid_ar_min, umid_ar_max, umid_solo_min, umid_solo_max):
        if temp_min > temp_max:
            raise ValueError("temp_ideal_min não pode ser maior que temp_ideal_max.")
        if umid_ar_min > umid_ar_max:
            raise ValueError("umidade_ideal_min não pode ser maior que umidade_ideal_max.")
        if umid_ar_min < 0 or umid_ar_max > 100:
            raise ValueError("Umidade deve estar entre 0 e 100.")
        if umid_solo_min > umid_solo_max:
            raise ValueError("umidade_ideal_min não pode ser maior que umidade_ideal_max.")
        if umid_solo_min < 0 or umid_solo_max > 100:
            raise ValueError("Umidade deve estar entre 0 e 100.")

    def _buscar_usuario(self, email):
        if not email:
            raise ValueError("usuario_email é obrigatório.")
        usuario = self.usuario_repository.buscar_por_email(email)
        if usuario is None:
            raise ValueError("Usuário não encontrado.")
        return usuario

    def criar(self, dados):
        fruta = (dados.get("fruta") or "").strip()
        status = (dados.get("status") or "").strip()

        if not fruta:
            raise ValueError("Fruta é obrigatória.")
        if not status:
            raise ValueError("Status é obrigatório.")

        temp_ideal_min = self._converter_float(dados.get("temp_ideal_min"), "temp_ideal_min")
        temp_ideal_max = self._converter_float(dados.get("temp_ideal_max"), "temp_ideal_max")
        umidade_ar_ideal_min = self._converter_float(dados.get("umidade_ar_ideal_min"), "umidade_ar_ideal_min")
        umidade_ar_ideal_max = self._converter_float(dados.get("umidade_ar_ideal_max"), "umidade_ar_ideal_max")
        umidade_solo_ideal_min = self._converter_float(dados.get("umidade_solo_ideal_min"), "umidade_solo_ideal_min")
        umidade_solo_ideal_max = self._converter_float(dados.get("umidade_solo_ideal_max"), "umidade_solo_ideal_max")

        self._validar_faixas(
            temp_ideal_min, temp_ideal_max,
            umidade_ar_ideal_min, umidade_ar_ideal_max,
            umidade_solo_ideal_min, umidade_solo_ideal_max,
        )

        usuario = self._buscar_usuario(dados.get("usuario_email"))

        lote = Lote(
            fruta=fruta,
            status=status,
            temp_ideal_min=temp_ideal_min,
            temp_ideal_max=temp_ideal_max,
            umidade_ar_ideal_min=umidade_ar_ideal_min,
            umidade_ar_ideal_max=umidade_ar_ideal_max,
            umidade_solo_ideal_min=umidade_solo_ideal_min,
            umidade_solo_ideal_max=umidade_solo_ideal_max,
            usuario_id=usuario.id
        )

        try:
            self.repository.cadastrar(lote)
            self.repository.commit()
            return lote
        except Exception:
            self.repository.rollback()
            raise

    def buscar_por_id(self, id):
        return self.repository.buscar_por_id(id)

    def buscar_todos(self):
        return self.repository.buscar_todos()

    def atualizar(self, id, dados):
        lote = self.repository.buscar_por_id(id)
        if lote is None:
            raise ValueError("Lote não encontrado.")

        if "fruta" in dados:
            fruta = (dados.get("fruta") or "").strip()
            if not fruta:
                raise ValueError("Fruta não pode ser vazia.")
            lote.fruta = fruta

        if "status" in dados:
            status = (dados.get("status") or "").strip()
            if not status:
                raise ValueError("Status não pode ser vazio.")
            lote.status = status

        if "temp_ideal_min" in dados:
            lote.temp_ideal_min = self._converter_float(dados["temp_ideal_min"], "temp_ideal_min")
        if "temp_ideal_max" in dados:
            lote.temp_ideal_max = self._converter_float(dados["temp_ideal_max"], "temp_ideal_max")
        if "umidade_ar_ideal_min" in dados:
            lote.umidade_ar_ideal_min = self._converter_float(dados["umidade_ar_ideal_min"], "umidade_ar_ideal_min")
        if "umidade_ar_ideal_max" in dados:
            lote.umidade_ar_ideal_max = self._converter_float(dados["umidade_ar_ideal_max"], "umidade_ar_ideal_max")
        if "umidade_solo_ideal_min" in dados:
            lote.umidade_solo_ideal_min = self._converter_float(dados["umidade_solo_ideal_min"], "umidade_solo_ideal_min")
        if "umidade_solo_ideal_max" in dados:
            lote.umidade_solo_ideal_max = self._converter_float(dados["umidade_solo_ideal_max"], "umidade_solo_ideal_max")

        self._validar_faixas(
            lote.temp_ideal_min, lote.temp_ideal_max,
            lote.umidade_ar_ideal_min, lote.umidade_ar_ideal_max,
            lote.umidade_solo_ideal_min, lote.umidade_solo_ideal_max

        )

        if "usuario_email" in dados:
            usuario = self._buscar_usuario(dados.get("usuario_email"))
            lote.usuario_id = usuario.id

        try:
            self.repository.atualizar(lote)
            self.repository.commit()
            return lote
        except Exception:
            self.repository.rollback()
            raise

    def deletar(self, id):
        lote = self.repository.buscar_por_id(id)
        if lote is None:
            raise ValueError("Lote não encontrado.")

        try:
            self.repository.deletar(lote)
            self.repository.commit()
            return True
        except Exception:
            self.repository.rollback()
            raise