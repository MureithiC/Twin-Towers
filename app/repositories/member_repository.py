from app.models.member import Member
from app import db

class MemberRepository:
    @staticmethod
    def get_all_members():
        return Member.query.all()

    @staticmethod
    def get_member_by_id(id):
        return Member.query.get(id)

    @staticmethod
    def create_member(member):
        db.session.add(member)
        db.session.commit()

    @staticmethod
    def update_member():
        db.session.commit()

    @staticmethod
    def find_by_email_or_phone(email, phone):
        return Member.query.filter((Member.email == email) | (Member.phone == phone)).first()

    @staticmethod
    def get_all_inactive_members():
        # Retrieve members where is_active is False
        return Member.query.filter_by(is_active=False).all()   