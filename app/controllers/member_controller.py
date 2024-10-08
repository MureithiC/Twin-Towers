from app.models.member import Member
from app import db

class MemberController:
    @staticmethod
    def soft_delete(member_id):
        member = Member.query.get_or_404(member_id)
        if not member.is_active:
            return {'message': 'Member is already soft deleted.'}, 400
        member.is_active = False
        db.session.commit()
        return {'message': f'Member {member_id} has been soft deleted successfully'}, 200

    @staticmethod
    def get_member(member_id):
        member = Member.query.get_or_404(member_id)
        if not member.is_active:
            return {'message': 'This member has been soft deleted.'}, 404
        return {
            'id': member.id,
            'name': member.name,
            'email': member.email,
            'is_active': member.is_active
        }

    @staticmethod
    def get_all_members():
        members = Member.query.filter_by(is_active=True).all()  # Fetch only active members
        return [
            {
                'id': member.id,
                'name': member.name,
                'email': member.email,
                'is_active': member.is_active
            } for member in members
        ]
