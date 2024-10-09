from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Member {self.name}>'