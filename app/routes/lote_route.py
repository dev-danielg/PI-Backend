from repositories import LoteRepository
from services import LoteService
from controllers import LoteController
from flask import Blueprint
from extensions import db
from middlewares import verificar_role

bp = Blueprint("lotes", __name__, url_prefix="/api/lotes")

@bp.routes("", methods=["POST"])
#@verificar_role("admin")
def cadastrar():
    repository = LoteRepository(db.session)
    service = LoteService(repository)
    controller = LoteController(repository, service)
    return controller.cadastrar()
