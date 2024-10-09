from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.models.member import Member

member_bp = Blueprint('members', __name__)

@member_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'supervisor' and password == 'password123':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(msg="Bad username or password"), 401

@member_bp.route('/members/<int:id>', methods=['PUT'])
@jwt_required()
def update_member(id):
    member = Member.query.get_or_404(id) 
    
    current_user = get_jwt_identity() 
    
    if current_user != 'supervisor':
        return jsonify(msg="You do not have permission to update this member"), 403

    data = request.json

    if 'name' in data:
        member.name = data['name']
    if 'phone' in data:
        member.phone = data['phone']
    if 'email' in data:
        member.email = data['email']

    if 'id' in data or 'role' in data:
        return jsonify(msg="You cannot update sensitive fields such as 'id' or 'role'"), 403

    try:
        db.session.commit()
        return jsonify({"message": f"Member {id} updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the member", "error": str(e)}), 500

# Adding GET for purpose of checking the updated info
@member_bp.route('/members', methods=['GET'])
@jwt_required()
def get_members():
    members = Member.query.all()  
    return jsonify([{
        'id': member.id,
        'name': member.name,
        'phone': member.phone,
        'email': member.email,
        'role': member.role,
    } for member in members]), 200