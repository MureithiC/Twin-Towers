from app.models.member import Member
from app import db

class MemberRepository:
    @staticmethod
    def get_all_members():
        """Retrieve all active members."""
        return Member.query.filter_by(is_active=True).all()

    @staticmethod
    def get_member_by_id(id):
        """Retrieve a member by their ID."""
        return Member.query.get(id)

    @staticmethod
    def create_member(member):
        """Create a new member and save it to the database."""
        db.session.add(member)
        db.session.commit()

    @staticmethod
    def update_member():
        """Commit changes to an existing member in the database."""
        db.session.commit()

    @staticmethod
    def find_by_email_or_phone(email, phone):
        """Check if a member with a specific email or phone number already exists."""
        return Member.query.filter((Member.email == email) | (Member.phone == phone)).first()

    @staticmethod
    def get_all_inactive_members():
        """Retrieve all members who are inactive (soft-deleted)."""
        return Member.query.filter_by(is_active=False).all()

    @staticmethod
    def get_members_by_role(role):
        """Retrieve all members who have a specific role."""
        return Member.query.filter_by(role=role, is_active=True).all()

    @staticmethod
    def find_by_email(email):
        """Retrieve a member by their email address."""
        return Member.query.filter_by(email=email).first()

