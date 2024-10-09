from app import db
from faker import Faker
import bcrypt

fake = Faker()

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")  # 'admin' or 'member'
    isActive = db.Column(db.Boolean, default=True)  # Soft-delete feature
    password_hash = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        """Serialize member object to dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "role": self.role,
            "isActive": self.isActive
        }
    
    # Hash and set the password
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Check if the password matches the hash
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    @classmethod
    def generate_fake_data(cls, count=1):
        """Generate and return fake member data."""
        fake_members = []
        for _ in range(count):
            member = cls(
                name=fake.name(),
                phone=fake.phone_number(),
                email=fake.unique.email(),
                role=fake.random_element(elements=("member", "admin")),
                isActive=fake.boolean(chance_of_getting_true=70)  # 70% chance to be active
            )
            member.set_password(fake.password())  # Set a random password
            fake_members.append(member)
        return fake_members
