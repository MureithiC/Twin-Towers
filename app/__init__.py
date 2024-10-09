from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.member_controller import member_bp

    # Register blueprints instead of adding routes manually
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(member_bp, url_prefix='/api/members')

    # Print out the registered routes for debugging
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")

    return app
