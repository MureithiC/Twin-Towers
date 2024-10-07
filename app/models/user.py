from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))  # Store hashed password
    role = db.Column(db.String(50), default='user')

    def __init__(self, email, password, role='user'):
        self.email = email
        self.set_password(password)  # Hash the password
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Use hash comparison

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role  
        }

    @staticmethod
    def is_password_strong(password):
        return (len(password) >= 8 and 
                re.search(r"[A-Z]", password) and 
                re.search(r"[a-z]", password) and 
                re.search(r"[0-9]", password))

    def __repr__(self):
        return f'<User {self.email}>'
