from flask_restful import Resource
from flask import request
from app.controllers.member_controller import MemberController
from app.models.member import Member  # Import the Member model
from app import db  # Import the db instance
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implement your authentication logic here
        # For simplicity, we'll assume the admin is always authenticated
        return f(*args, **kwargs)
    return decorated_function

class MemberResource(Resource):
    @admin_required
    def delete(self, id):
        return MemberController.soft_delete(id)

    @admin_required
    def get(self, id):
        return MemberController.get_member(id)

    @admin_required
    def post(self):
        data = request.get_json()
        new_member = Member(name=data['name'], email=data['email'])
        db.session.add(new_member)
        db.session.commit()
        return {'message': 'Member created successfully.', 'id': new_member.id}, 201

class MemberListResource(Resource):
    @admin_required
    def get(self):
        # Fetch all members (active members only)
        members = Member.query.filter_by(is_active=True).all()
        return [
            {
                'id': member.id,
                'name': member.name,
                'email': member.email,
                'is_active': member.is_active
            } for member in members
        ], 200
