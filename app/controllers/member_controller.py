import logging
from flask_restful import Resource
from app.repositories.member_repository import MemberRepository
from flask import jsonify
from flask_jwt_extended import jwt_required
from app.utils.validation_utils import admin_required

def create_response(data, status_code):
    """Helper function to create a standardized JSON response."""
    return jsonify(data), status_code

class InactiveMemberResource(Resource):
    @jwt_required()  # Ensure authentication
    @admin_required  # Ensure user is an admin
    def get(self):
        """
        Handles GET /members/inactive to retrieve all inactive members.
        Returns a list of inactive members.
        """
        inactive_members = MemberRepository.get_inactive_members()
        
        if not inactive_members:
            logging.info("No inactive members found.")
            return create_response({'message': 'No inactive members found'}, status_code=404)

        logging.info(f"Retrieved {len(inactive_members)} inactive members.")
        return create_response({
            'members': [member.to_dict() for member in inactive_members]
        }, status_code=200)

class MemberResource(Resource):
    def get(self):
        """
        Handles GET /members to retrieve all members.
        Returns a list of all members.
        """
        members = MemberRepository.get_all_members()

        logging.info(f"Retrieved {len(members)} members.")
        return create_response({
            'members': [member.to_dict() for member in members]
        }, status_code=200)
