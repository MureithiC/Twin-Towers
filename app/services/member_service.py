from app.repositories.member_repository import MemberRepository
from app.models.member import Member

class MemberService:
    @staticmethod
    def get_all_members():
        return MemberRepository.get_all_members()

    @staticmethod
    def get_member_by_id(id):
        member = MemberRepository.get_member_by_id(id)
        if not member:
            return {"error": "Member not found"}, 404
        return member.to_dict(), 200

    @staticmethod
    def create_member(data):
        required_fields = ['name', 'phone', 'email', 'role']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"'{field}' is required"}, 400

        if MemberRepository.find_by_email_or_phone(data['email'], data['phone']):
            return {"error": "Email or Phone already exists"}, 400

        try:
            member = Member(
                name=data['name'],
                phone=data['phone'],
                email=data['email'],
                role=data.get('role', 'member')
            )

            member.set_password(data['password'])
            
            MemberRepository.create_member(member)
            return member.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_member(id, data):
        member = MemberRepository.get_member_by_id(id)
        if not member:
            return {"error": "Member not found"}, 404

        if MemberRepository.find_by_email_or_phone(data['email'], data['phone']):
            return {"error": "Email or Phone already exists"}, 400

        member.name = data.get('name', member.name)
        member.phone = data.get('phone', member.phone)
        member.email = data.get('email', member.email)
        
        MemberRepository.update_member()
        return member.to_dict(), 200

    @staticmethod
    def assign_role(member_id, new_role):
        member = MemberRepository.get_member_by_id(member_id)
        if not member:
            return {"error": "Member not found"}, 404
        
        if new_role not in Member.get_all_roles():
            return {"error": "Invalid role"}, 400
        
        member.role = new_role
        MemberRepository.update_member()
        return {"message": "Role assigned successfully"}, 200

    @staticmethod
    def get_available_roles():
        return {"roles": Member.get_all_roles()}, 200

    @staticmethod
    def get_members_by_role(role):
        if role not in Member.get_all_roles():
            return {"error": "Invalid role"}, 400
        
        members = MemberRepository.get_members_by_role(role)
        return {"members": [member.to_dict() for member in members]}, 200

    @staticmethod
    def get_member_role(member_id):
        member = MemberRepository.get_member_by_id(member_id)
        if not member:
            return {"error": "Member not found"}, 404
        return {"role": member.role}, 200

    
    @staticmethod
    def get_inactive_members():
        # Get the list of inactive members from the repository
        inactive_members = MemberRepository.get_all_inactive_members()
        # Convert each member object to a dictionary for JSON response
        return [member.to_dict() for member in inactive_members], 200
    

@staticmethod
def authenticate_admin(email, password):
    member = MemberRepository.find_by_email(email)
    if member and member.role == 'admin' and member.check_password(password):
        return member
    return None
