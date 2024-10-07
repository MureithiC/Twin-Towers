
from flask_restful import Api
from flask import Blueprint
from .member_controller import InactiveMemberResource, MemberResource
from .auth_controller import LoginResource, RegisterResource

api = Api()

def register_routes(app):
    api.add_resource(LoginResource, '/login')
    
    api.add_resource(RegisterResource, '/register')
    
    api.add_resource(InactiveMemberResource, '/members/inactive')
    api.add_resource(MemberResource, '/members')
    
    api.init_app(app)