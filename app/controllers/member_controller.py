from flask import request, jsonify, session
from flask_restful import Resource
from models.member import db, User
from faker import Faker

fake = Faker()

class Register(Resource):
    def post(self):
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
        data = request.get_json()
        
        if data is None:
            return {"error": "No JSON data provided."}, 400
        
        username = data.get('username')
        user = User.query.filter_by(username=username).first()

        if user:
            session['user_id'] = user.id
            return {"message": "Logged in successfully."}, 200
        
        return {"error": "Invalid credentials."}, 401

class GetUsers(Resource):
    def get(self):
        users = User.query.all()
        users_list = [{"id": user.id, "username": user.username} for user in users]
        return jsonify(users_list)

class UpdateUser(Resource):
    def put(self, user_id):
        current_user_id = session.get('user_id')
        if current_user_id is None:
            return {"error": "User not logged in."}, 401

        user = db.session.get(User, user_id)
        if not user:
            return {"error": "User not found."}, 404

        data = request.get_json()

        if 'username' in data:
            new_username = data['username']
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user.id:
                return {"error": "Username already exists."}, 400
            
            user.username = new_username

        if 'role' in data:
            if user.id == current_user_id:
                return {"error": "You cannot update your own role."}, 403

        if 'status' in data:
            if user.id == current_user_id:
                return {"error": "You cannot update your own status."}, 403

        db.session.commit()
        return {"message": "User updated successfully."}, 200
