from flask import Blueprint, request, jsonify
from app.services.member_service import MemberService
from app.utilis.authentication import authenticate_admin
from app.utilis.validation_utils import validate_required_fields

member_bp = Blueprint('member', __name__)

@member_bp.route('/', methods=['GET'])
@authenticate_admin()
def get_all_members():
    members = MemberService.get_all_members()
    return jsonify([member.to_dict() for member in members]), 200

@member_bp.route('/<int:id>', methods=['GET'])
@authenticate_admin()
def get_member(id):
    return MemberService.get_member_by_id(id)

@member_bp.route('/', methods=['POST'])
@authenticate_admin()
def create_member():
    data = request.json
    valid, error = validate_required_fields(data, ['name', 'phone', 'email', 'password', 'role'])
    if not valid:
        return jsonify({"error": error}), 400
    return MemberService.create_member(data)

@member_bp.route('/<int:id>', methods=['PUT'])
@authenticate_admin()
def update_member(id):
    data = request.json
    return MemberService.update_member(id, data)

@member_bp.route('/assign_role', methods=['POST'])
@authenticate_admin()
def assign_role():
    data = request.json
    valid, error = validate_required_fields(data, ['member_id', 'new_role'])
    if not valid:
        return jsonify({"error": error}), 400
    return MemberService.assign_role(data['member_id'], data['new_role'])

@member_bp.route('/available_roles', methods=['GET'])
@authenticate_admin()
def get_available_roles():
    return MemberService.get_available_roles()

@member_bp.route('/members_by_role/<role>', methods=['GET'])
@authenticate_admin()
def get_members_by_role(role):
    return MemberService.get_members_by_role(role)

@member_bp.route('/member_role/<int:member_id>', methods=['GET'])
@authenticate_admin()
def get_member_role(member_id):
    return MemberService.get_member_role(member_id)

@member_bp.route('/inactive', methods=['GET'])
@authenticate_admin()
def get_inactive_members():
    """Retrieve inactive members (is_active=False)."""
    inactive_members, status_code = MemberService.get_inactive_members()
    return jsonify(inactive_members), status_code

from flask import request, jsonify
from flask_jwt_extended import create_access_token

@member_bp.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    valid, error = validate_required_fields(data, ['email', 'password'])
    if not valid:
        return jsonify({"error": error}), 400
    
    admin = MemberService.authenticate_admin(data['email'], data['password'])
    if admin:
        access_token = create_access_token(identity=admin.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
