from app.models.member import Member, db

class MemberRepository:
    @staticmethod
    def get_member(member_id):
        return Member.query.get(member_id)

    @staticmethod
    def update_member(member):
        db.session.commit()