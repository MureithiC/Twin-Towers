from app.repositories.member_repository import MemberRepository

class MemberService:
    @staticmethod
    def get_inactive_members():
        """
        Fetch all inactive members.
        """
        return MemberRepository.get_inactive_members()

    @staticmethod
    def restore_member(member_id):
        """
        Restore a soft-deleted member.
        """
        member = MemberRepository.get_member_by_id(member_id)
        if member and not member.is_active:
            member.is_active = True
            return member.save()
        return None
