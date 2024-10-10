from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from functools import wraps

def authenticate_admin():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] != 'admin':
                return jsonify({"error": "Admin access required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper