from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from app.models.member import db
from app.controllers.member_controller import Register, Login, GetUsers, UpdateUser
from app.controllers.auth_controller import auth_bp
from extensions import DATABASE

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    api = Api(app)
    api.add_resource(Register, '/api/register')
    api.add_resource(Login, '/api/login')
    api.add_resource(GetUsers, '/api/users')
    api.add_resource(UpdateUser, '/api/update_user/<int:user_id>')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        
    app.run(port=5000, debug=True)
