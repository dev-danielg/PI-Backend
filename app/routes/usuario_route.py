from app.repositories import UsuarioRepository
from app.services import UsuarioService
from app.controllers import UsuarioController
from flask import Blueprint
from app.extensions import db
from app.middlewares import verificar_role


bp = Blueprint("usuario", __name__, url_prefix="/api/usuarios")


@bp.route("", methods=["POST"])
@verificar_role("admin")
def cadastrar():
    repository = UsuarioRepository(db.session)
    service = UsuarioService(repository)
    controller = UsuarioController(repository, service)
    return controller.cadastrar()