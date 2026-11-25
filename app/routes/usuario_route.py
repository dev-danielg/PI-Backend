from app.repositories import UsuarioRepository
from app.services import UsuarioService
from app.controllers import UsuarioController
from flask import Blueprint
from app.extensions import db
from app.middlewares import verificar_role


bp = Blueprint("usuario", __name__, url_prefix="/api/usuarios")


@bp.route("", methods=["POST"])
#@verificar_role("admin")
def cadastrar():
    repository = UsuarioRepository(db.session)
    service = UsuarioService(repository)
    controller = UsuarioController(repository, service)
    return controller.cadastrar()


@bp.route("", methods=["GET"])
def buscar_todos():
    repository = UsuarioRepository(db.session)
    service = UsuarioService(repository)
    controller = UsuarioController(repository, service)
    return controller.buscar_todos()


@bp.route("/<int:id_usuario>", methods=["DELETE"])
def deletar(id_usuario):
    repository = UsuarioRepository(db.session)
    service = UsuarioService(repository)
    controller = UsuarioController(repository, service)
    return controller.deletar(id_usuario)


@bp.route("/<int:id_usuario>", methods=["PUT"])
def atualizar(id_usuario):
    repository = UsuarioRepository(db.session)
    service = UsuarioService(repository)
    controller = UsuarioController(repository, service)
    return controller.atualizar(id_usuario)