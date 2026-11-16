from flask import Blueprint
from app.repositories import SensorRepository, LoteRepository
from app.services import SensorService
from app.controllers import SensorController
from app.extensions import db

bp = Blueprint("sensores", __name__, url_prefix="/api/sensores")


def _controller():
    sensor_repo = SensorRepository(db.session)
    lote_repo = LoteRepository(db.session)
    service = SensorService(sensor_repo, lote_repo)
    return SensorController(service)


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