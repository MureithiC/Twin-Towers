from flask import Blueprint, request, jsonify, session
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.member_service import MemberService
from app.models.member import Member
from app import db


member_bp = Blueprint('member_bp', __name__)  
member_api = Api(member_bp)  

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')

        if Member.query.filter_by(username=username).first():
            return {"error": "Member already exists."}, 400

        new_member = Member(username=username)
        db.session.add(new_member)
        db.session.commit()
        return {"message": "Member registered successfully."}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()

        if data is None:
            return {"error": "No JSON data provided."}, 400

        username = data.get('username')
        member = Member.query.filter_by(username=username).first()

        if member:
            session['member_id'] = member.id
            return {"message": "Logged in successfully."}, 200
        
        return {"error": "Invalid credentials."}, 401

class MemberListResource(Resource):
    @jwt_required()
    def get(self):
        members = MemberService.get_all_members()
        return [member.to_dict() for member in members], 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        data = request.get_json()
        return MemberService.create_member(data)

class MemberResource(Resource):
    @jwt_required()
    def get(self, id):
        return MemberService.get_member_by_id(id)

    @jwt_required()
    def put(self, id):
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
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        inactive_members, status_code = MemberService.get_inactive_members()
        return inactive_members, status_code

class UpdateMember(Resource):
    @jwt_required()
    def put(self, member_id):
        current_member_id = get_jwt_identity()['id']
        
        if current_member_id is None:
            return {"error": "Member not logged in."}, 401

        member = db.session.get(Member, member_id)
        if not member:
            return {"error": "Member not found."}, 404

        data = request.get_json()

        if 'role' in data or 'status' in data:
            return {"error": "You cannot update your own role or status."}, 403

        if 'username' in data:
            new_username = data['username']
            existing_member = Member.query.filter_by(username=new_username).first()
            if existing_member and existing_member.id != member.id:
                return {"error": "Username already exists."}, 400
            member.username = new_username

        db.session.commit()
        return {"message": "Member updated successfully."}, 200

member_api.add_resource(Register, '/register')
member_api.add_resource(Login, '/login')
member_api.add_resource(MemberListResource, '/members')
member_api.add_resource(MemberResource, '/members/<int:id>')
member_api.add_resource(InactiveMemberResource, '/members/inactive')
member_api.add_resource(UpdateMember, '/members/<int:member_id>')
