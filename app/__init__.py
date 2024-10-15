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
    
    # Initialize JWT for authentication
    jwt = JWTManager(app)

    # Import controllers and blueprints
    from app.controllers.member_controller import MemberListResource, MemberResource, InactiveMemberResource
    from app.controllers.auth_controller import auth_bp
    from app.routes.member_routes import member_bp
    
    # Set up RESTful API
    api = Api(app)
    
    # Define resources for member operations
    api.add_resource(MemberListResource, '/members')
    api.add_resource(MemberResource, '/members/<int:id>')
    api.add_resource(InactiveMemberResource, '/members/inactive')

    # Register blueprints
    app.register_blueprint(auth_bp)  # Authentication-related routes
    app.register_blueprint(member_bp, url_prefix='/members')  # Member-related routes
    
    # Set JWT identity claims for further use in the app
    @jwt.user_identity_loader
    def user_identity_lookup(member):
        return {"id": member.id, "email": member.email, "role": member.role}

    # Configure JWT additional claims to check admin role
    @jwt.additional_claims_loader
    def add_claims_to_jwt(member):
        return {"role": member.role}

    # Register error handlers for unauthorized access
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({"error": "Unauthorized access. Please log in."}), 401
    
    return app
