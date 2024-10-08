from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from app.models.member import Member
from app.utils.validation_utils import paginate

class MemberResource(Resource):
    @jwt_required()
    def get(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('limit', type=int, default=20, location='args')
        args = parser.parse_args()

        members_data = Member.get_active_members()

        paginated_data = paginate(members_data, args['page'], args['limit'])

        return paginated_data, 200

class UserLogin(Resource):
    def post(self):
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username == 'supervisor' and password == 'password123':
            access_token = create_access_token(identity=username)
            return {"access_token": access_token}, 200
        else:
            return {"msg": "Invalid username or password"}, 401
