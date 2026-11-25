from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.repositories import UsuarioRepository
from app.services import AuthService
from app.controllers import AuthController
from app.extensions import db


bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _controller():
    repository = UsuarioRepository(db.session)
    service = AuthService(repository)
    return AuthController(service)


@bp.route("", methods=["POST"])
def login():
    return _controller().login()


@bp.route("/mfa/verificar", methods=["POST"])
def mfa_verificar():
    return _controller().verificar_mfa()


@bp.route("/mfa/setup", methods=["POST"])
@jwt_required()
def mfa_setup():
    return _controller().iniciar_mfa()


@bp.route("/mfa/ativar", methods=["POST"])
@jwt_required()
def mfa_ativar():
    return _controller().ativar_mfa()


@bp.route("/mfa/desativar", methods=["POST"])
@jwt_required()
def mfa_desativar():
    return _controller().desativar_mfa()
