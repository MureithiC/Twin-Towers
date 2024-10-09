from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required
from app.services.member_service import MemberService

from flask import Blueprint, jsonify, request
from app.models.member import Member

# Blueprint setup
member_bp = Blueprint('member_bp', __name__)
member_api = Api(member_bp)

class InactiveMembersController(Resource):
    @jwt_required()
    
    def get(self):
        print("InactiveMembersController GET method called")
        # Retrieve inactive members via the service layer
        inactive_members = MemberService.get_inactive_members()
        print(f"Inactive Members: {inactive_members}")
        return jsonify({"members": [member.to_dict() for member in inactive_members]})

# Register the resource with the API
member_api.add_resource(InactiveMembersController, '/inactive-members')