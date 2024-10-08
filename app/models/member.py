
from extensions import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50))
    status = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.username}>'
