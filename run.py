from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from app.models.member import db
from app.controllers.member_controller import Register, Login, GetUsers, UpdateUser
from extensions import DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GetUsers, '/users')
api.add_resource(UpdateUser, '/update_user/<int:user_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(port=5000, debug=True)
