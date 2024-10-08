from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config
from app.controllers.member_controller import UserLogin
from app.controllers.member_controller import MemberResource

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)

jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')  
api.add_resource(MemberResource, '/members')  

if __name__ == "__main__":
    app.run(debug=True)
