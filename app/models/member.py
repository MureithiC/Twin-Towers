from app import db
from faker import Faker
import bcrypt

fake = Faker()

class Member(db.Model):
    """Represents a member in the system, including user-related attributes."""
    __tablename__ = 'member'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")
    password_hash = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Member {self.username}>'

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "is_active": self.is_active 
        }

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    @classmethod
    def generate_fake_data(cls):
        return cls(
            username=fake.user_name(),
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            role=fake.random_element(elements=("member", "admin")),
            password_hash=fake.password()
        )

    @classmethod
    def get_all_roles(cls):
        return ["member", "admin"] 

    def assign_role(self, new_role):
        if new_role in self.get_all_roles():
            self.role = new_role
            db.session.commit()
            return True
        return False

    @classmethod
    def get_members_by_role(cls, role):
        return cls.query.filter_by(role=role).all()

    @classmethod
    def change_role(cls, member_id, new_role):
        member = cls.query.get(member_id)
        if member and new_role in cls.get_all_roles():
            member.role = new_role
            db.session.commit()
            return True
        return False
