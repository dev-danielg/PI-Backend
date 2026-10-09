from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .extensions import db, jwt
from datetime import timedelta


def create_app():
    
    app = Flask(__name__)
    CORS(app)


    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)


    db.init_app(app)
    jwt.init_app(app)

    from models import Usuario, Registro, Lote, Sensor
    with app.app_context():
        db.create_all()
    
    
    from routes import bp_auth, bp_usuario
    app.register_blueprint(bp_usuario)
    app.register_blueprint(bp_auth)
    
    return app
