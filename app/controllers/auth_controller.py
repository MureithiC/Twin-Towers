# from flask import request, jsonify, Blueprint
# from flask_restful import Resource, Api
# from flask_jwt_extended import create_access_token
# from app.services.member_service import MemberService
# from app.utils.validation_utils import validate_login
# from app.models.member import Member
# from werkzeug.security import check_password_hash

# # Blueprint setup
# auth_bp = Blueprint('auth_bp', __name__)
# auth_api = Api(auth_bp)


# class AuthController(Resource):
#     def post(self):
#         # Get JSON data from the request
#         data = request.get_json()

#         try:
#             # Validate incoming login data
#             validate_login(data)
#         except ValidationError as e:
#             return jsonify({"errors": e.errors}), 400  # Return the validation errors

#         # Extract email and password from the request
#         email = data.get('email')
#         password = data.get('password')

#         # Check if both email and password are provided
#         if not email or not password:
#             return jsonify({"error": "Email and password are required"}), 400

#         # Find the member by email
#         member = MemberService.find_by_email(email)

#         if not member:
#             return jsonify({"error": "Invalid credentials"}), 401

#         if member.role != 'admin':
#             return jsonify({"error": "Admin access required"}), 403

#         # Check if password_hash is not empty
#         if not member.password_hash:
#             return jsonify({"error": "User account is not properly configured"}), 500

#         # Use the Member's check_password method
#         if member.check_password(password):
#             access_token = create_access_token(identity={"id": member.id, "role": member.role})
#             return jsonify(access_token=access_token), 200
#         else:
#             return jsonify({"error": "Invalid password"}), 401

# # Register the AuthController resource with the API
# auth_api.add_resource(AuthController, '/login')

# # In your main app setup, don't forget to register the blueprint
# # app.register_blueprint(auth_bp, url_prefix='/api/auth')
from flask import request, Blueprint
from flask_restful import Resource, Api
from app.models.member import Member
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)
auth_api = Api(auth_bp)

class AuthResource(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        member = Member.query.filter_by(email=email).first()

        if member and member.role == 'admin' and member.check_password(password):
            access_token = create_access_token(identity={"id": member.id, "role": member.role})
            return {"access_token": access_token}, 200

        return {"error": "Invalid credentials or admin access required"}, 401

# Add the resource to the API
auth_api.add_resource(AuthResource, '/login')