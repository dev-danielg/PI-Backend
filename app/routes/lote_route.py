from flask import Blueprint, request
from app.repositories import LoteRepository, UsuarioRepository
from app.services import LoteService
from app.controllers import LoteController
from app.extensions import db

bp = Blueprint("lotes", __name__, url_prefix="/api/lotes")


def _controller():
    lote_repo = LoteRepository(db.session)
    usuario_repo = UsuarioRepository(db.session)
    service = LoteService(lote_repo, usuario_repo)
    return LoteController(service)


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