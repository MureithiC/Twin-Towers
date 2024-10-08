from app import create_app
from app.controllers.auth_controller import auth_bp
from app.controllers.member_controller import member_bp


app = create_app()

app.register_blueprint(member_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)