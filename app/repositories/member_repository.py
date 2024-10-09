from app.models.member import Member
from app import db

class MemberRepository:
    @staticmethod
    def get_inactive_members():
        """Retrieve all members where isActive is False."""
        return Member.query.filter_by(isActive=False).all()

    @staticmethod
    def find_by_email(email):
        """Find a member by their email."""
        return Member.query.filter_by(email=email).first()
