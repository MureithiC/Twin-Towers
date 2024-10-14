from flask import Blueprint, request, jsonify, session
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.member_service import MemberService
from app.models.member import Member
from app import db
from models.member import User

member_bp = Blueprint('member_bp', __name__)  
member_api = Api(member_bp)  

class Register(Resource):
    def post(self):
        """Register a new user."""
        data = request.get_json()
        username = data.get('username')

        if User.query.filter_by(username=username).first():
            return {"error": "User already exists."}, 400

        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User registered successfully."}, 201

class Login(Resource):
    def post(self):
        """Log in a user."""
        data = request.get_json()

        if data is None:
            return {"error": "No JSON data provided."}, 400

        username = data.get('username')
        user = User.query.filter_by(username=username).first()

        if user:
            session['user_id'] = user.id
            return {"message": "Logged in successfully."}, 200
        
        return {"error": "Invalid credentials."}, 401

class MemberListResource(Resource):
    @jwt_required()
    def get(self):
        """Get all members."""
        members = MemberService.get_all_members()
        return [member.to_dict() for member in members], 200

    @jwt_required()
    def post(self):
        """Create a new member (admin-only)."""
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        data = request.get_json()
        return MemberService.create_member(data)

class MemberResource(Resource):
    @jwt_required()
    def get(self, id):
        """Get a single member by ID."""
        return MemberService.get_member_by_id(id)

    @jwt_required()
    def put(self, id):
        """Update a member by ID (admin-only)."""
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        member = Member.query.get(id)
        if not member:
            return {"error": "Member not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "Invalid request, no data provided"}, 400

        if 'phone' in data and Member.query.filter(Member.phone == data['phone'], Member.id != member.id).first():
            return {"error": "Phone number already exists"}, 400

        if 'email' in data and Member.query.filter(Member.email == data['email'], Member.id != member.id).first():
            return {"error": "Email address already exists"}, 400

        member.name = data.get('name', member.name)
        member.phone = data.get('phone', member.phone)
        member.email = data.get('email', member.email)
        member.role = data.get('role', member.role)

        try:
            db.session.commit()
            return member.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": "An error occurred while updating the member", "details": str(e)}, 500

class InactiveMemberResource(Resource):
    @jwt_required()
    def get(self):
        """Get all inactive members (admin-only)."""
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        inactive_members, status_code = MemberService.get_inactive_members()
        return inactive_members, status_code

class UpdateUser(Resource):
    @jwt_required()
    def put(self, user_id):
        """Update a user (non-admin)."""
        current_user_id = get_jwt_identity()['id']
        
        if current_user_id is None:
            return {"error": "User not logged in."}, 401

        user = db.session.get(User, user_id)
        if not user:
            return {"error": "User not found."}, 404

        data = request.get_json()

        if 'role' in data or 'status' in data:
            return {"error": "You cannot update your own role or status."}, 403

        if 'username' in data:
            new_username = data['username']
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user.id:
                return {"error": "Username already exists."}, 400
            user.username = new_username

        db.session.commit()
        return {"message": "User updated successfully."}, 200

member_api.add_resource(Register, '/register')
member_api.add_resource(Login, '/login')
member_api.add_resource(MemberListResource, '/members')
member_api.add_resource(MemberResource, '/members/<int:id>')
member_api.add_resource(InactiveMemberResource, '/members/inactive')
member_api.add_resource(UpdateUser, '/users/<int:user_id>')
