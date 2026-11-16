from flask import Blueprint
from app.repositories import RegistroRepository, SensorRepository, LoteRepository
from app.services import RegistroService
from app.controllers import RegistroController
from app.extensions import db

bp = Blueprint("registros", __name__, url_prefix="/api/registros")


def _controller():
    registro_repo = RegistroRepository(db.session)
    sensor_repo = SensorRepository(db.session)
    lote_repo = LoteRepository(db.session)
    service = RegistroService(registro_repo, sensor_repo, lote_repo)
    return RegistroController(service)

@bp.route("", methods=["POST"])
# @verificar_role("admin")
def cadastrar():
    return _controller().cadastrar()

@bp.route("", methods=["GET"])
# @verificar_role("admin")
def buscar_todos():
    return _controller().buscar_todos()

@bp.route("/<int:id>", methods=["GET"])
# @verificar_role("admin")
def buscar_por_id(id):
    return _controller().buscar_por_id(id)

@bp.route("/<int:id>", methods=["PUT", "PATCH"])
# @verificar_role("admin")
def atualizar(id):
    return _controller().atualizar(id)

@bp.route("/<int:id>", methods=["DELETE"])
# @verificar_role("admin")
def deletar(id):
    return _controller().deletar(id)

@bp.route("/sensor/<int:sensor_id>", methods=["GET"])
# @verificar_role("admin")
def buscar_por_sensor(sensor_id):
    return _controller().buscar_por_sensor(sensor_id)

@bp.route("/thingspeak/<int:sensor_id>", methods=["POST"])
# @verificar_role("admin")
def cadastrar_thingspeak(sensor_id):
    return _controller().cadastrar_thingspeak(sensor_id)

@bp.route("/thingspeak/<int:sensor_id>/sync", methods=["POST"])
# @verificar_role("admin")
def sincronizar_thingspeak(sensor_id):
    return _controller().sincronizar_thingspeak(sensor_id)