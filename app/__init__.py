from flask import Flask
from flask_jwt_extended import JWTManager
from app.models.member import db
from app.controllers.member_controller import member_bp
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(member_bp)

    return app