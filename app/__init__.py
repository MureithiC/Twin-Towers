from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Import the resources (views)
    from app.views.member_view import MemberResource, MemberListResource
    api = Api(app)

    # Register the routes
    api.add_resource(MemberResource, '/members/<int:id>')  # Individual member routes
    api.add_resource(MemberListResource, '/members')  # List all members

    return app
