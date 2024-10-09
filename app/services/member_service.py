from app.repositories.member_repository import MemberRepository

class MemberService:
    @staticmethod
    def get_inactive_members():
        """Get all members who are inactive (isActive=False)."""
        return MemberRepository.get_inactive_members()

    @staticmethod
    def find_by_email(email):
        """Find a member by their email."""
        return MemberRepository.find_by_email(email)
