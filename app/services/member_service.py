from models import Member, db

def soft_delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    member.soft_delete()
    db.session.commit()
    return {"message": "Member has been soft deleted"}

def get_members(include_inactive=False):
    if include_inactive:
        members = Member.query.all()
    else:
        members = Member.query.filter_by(isActive=True).all()
    
    return [{"id": member.id, "name": member.name, "email": member.email} for member in members]
