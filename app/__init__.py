from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    jwt = JWTManager(app)

    from app.controllers.member_controller import MemberListResource, MemberResource, InactiveMemberResource 
    from app.controllers.auth_controller import auth_bp
    from app.routes.member_routes import member_bp
    
    api = Api(app)
    api.add_resource(MemberListResource, '/members')
    api.add_resource(MemberResource, '/members/<int:id>')
    api.add_resource(InactiveMemberResource, '/members/inactive') 

    app.register_blueprint(auth_bp)
    app.register_blueprint(member_bp, url_prefix='/members')
     
    return app