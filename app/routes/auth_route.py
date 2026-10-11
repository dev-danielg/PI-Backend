from flask import Blueprint
from app.repositories import UsuarioRepository
from app.services import AuthService
from app.controllers import AuthController
from app.extensions import db


bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.route("", methods=["POST"])
def login():
    repository = UsuarioRepository(db.session)
    service = AuthService(repository)
    controller = AuthController(service)
    return controller.login()
