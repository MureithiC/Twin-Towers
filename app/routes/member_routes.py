from flask import Blueprint, request, jsonify
from app.services.member_service import MemberService
from app.utilis.authentication import authenticate_admin
from app.utilis.validation_utils import validate_required_fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

member_bp = Blueprint('member', __name__)

@member_bp.route('/', methods=['GET'])
@jwt_required()
@authenticate_admin()
def get_all_members():
    members = MemberService.get_all_members()
    return jsonify([member.to_dict() for member in members]), 200

@member_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@authenticate_admin()
def get_member(id):
    return MemberService.get_member_by_id(id)

@member_bp.route('/', methods=['POST'])
@jwt_required()
@authenticate_admin()
def create_member():
    data = request.json
    valid, error = validate_required_fields(data, ['name', 'phone', 'email', 'password', 'role'])
    if not valid:
        return jsonify({"error": error}), 400
    return MemberService.create_member(data)

@member_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@authenticate_admin()
def update_member(id):
    data = request.json
    return MemberService.update_member(id, data)

@member_bp.route('/assign_role', methods=['POST'])
@jwt_required()
@authenticate_admin()
def assign_role():
    data = request.json
    valid, error = validate_required_fields(data, ['member_id', 'new_role'])
    if not valid:
        return jsonify({"error": error}), 400
    
    current_user = get_jwt_identity()  # Get current logged-in user's info
    return MemberService.assign_role(data['member_id'], data['new_role'], current_user['email'], current_user['password'])

@member_bp.route('/available_roles', methods=['GET'])
@jwt_required()
@authenticate_admin()
def get_available_roles():
    return MemberService.get_available_roles()

@member_bp.route('/members_by_role/<role>', methods=['GET'])
@jwt_required()
@authenticate_admin()
def get_members_by_role(role):
    return MemberService.get_members_by_role(role)

@member_bp.route('/member_role/<int:member_id>', methods=['GET'])
@jwt_required()
@authenticate_admin()
def get_member_role(member_id):
    return MemberService.get_member_role(member_id)

@member_bp.route('/inactive', methods=['GET'])
@jwt_required()
@authenticate_admin()
def get_inactive_members():
    """Retrieve inactive members (is_active=False)."""
    inactive_members, status_code = MemberService.get_inactive_members()
    return jsonify(inactive_members), status_code

@member_bp.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    valid, error = validate_required_fields(data, ['email', 'password'])
    if not valid:
        return jsonify({"error": error}), 400
    
    admin = MemberService.authenticate_admin(data['email'], data['password'])
    if admin:
        access_token = create_access_token(identity={'id': admin.id, 'email': admin.email, 'role': admin.role})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
