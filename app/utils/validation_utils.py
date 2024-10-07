from functools import wraps
from flask import abort, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def validate_member_data(data):
    """
    Validate member data before processing.
    """
    if not data.get('name'):
        abort(400, description="Member name is required.")
    if not data.get('email'):
        abort(400, description="Member email is required.")
    # Add more validation as needed


def validate_is_admin(user):
    """
    Check if the user has admin privileges.
    """
    if not user.is_admin:
        abort(403, description="Admin access required.")


def admin_required(f):
    """
    Decorator to restrict access to admin users only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        
        if user is None:
            return jsonify({"msg": "User not found."}), 404  # User not found
        if user.role != 'admin':
            return jsonify({"msg": "Admins only!"}), 403

        return f(*args, **kwargs)

    return decorated_function
