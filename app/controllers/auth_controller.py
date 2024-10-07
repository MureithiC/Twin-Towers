import logging
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from app.models.user import User
from app import db

class RegisterResource(Resource):
    def post(self):
        try:
            # Get the data from the request
            data = request.get_json()

            # Validate the input data
            if not data or 'email' not in data or 'password' not in data:
                return jsonify({'msg': 'Missing email or password'}), 400

            email = data['email']
            password = data['password']

            # Check if the user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'msg': 'User already exists'}), 400

            # Create a new user instance
            new_user = User(email=email, password=password)  # Set the password directly
            db.session.add(new_user)
            db.session.commit()

            logging.info(f"User {email} created successfully.")
            return jsonify({'msg': 'User created successfully'}), 201
        except Exception as e:
            logging.error(f"Error during registration: {e}")
            return jsonify({'msg': 'Internal Server Error'}), 500


class LoginResource(Resource):
    def post(self):
        # Attempt to get JSON data from the request
        data = request.get_json()

        # Check for missing email or password in the request
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'msg': 'Missing email or password'}), 400
        
        email = data['email']
        password = data['password']

        # Retrieve the user from the database
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and if the password is correct
        if not user or not user.check_password(password):
            return jsonify({'msg': 'Bad email or password'}), 401
        
        # Create an access token for the user
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})

        logging.info(f"User {email} logged in successfully.")
        return jsonify({
            'user': user.to_dict(),  # Ensure this returns a simple dict
            'access_token': access_token
        }), 200
