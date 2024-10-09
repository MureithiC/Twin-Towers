from app.repositories.member_repository import MemberRepository
from app.models.member import Member

class MemberService:
    @staticmethod
    def update_member(member_id, data):
        member = MemberRepository.get_member(member_id)
        if not member:
            return None
        
        # just non-sensitive 
        member.name = data.get('name', member.name)
        member.phone = data.get('phone', member.phone)
        member.email = data.get('email', member.email)

        MemberRepository.update_member(member)
        return member