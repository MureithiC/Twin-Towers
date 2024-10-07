from app.models.member import Member  # Adjust path as needed
from app import db

class MemberRepository:
    @staticmethod
    def get_inactive_members():
        """
        Fetches a list of members who have is_active set to False.
        :return: A list of inactive members.
        """
        return Member.query.filter_by(is_active=False).all()  # Return all inactive members

    @staticmethod
    def get_member_by_id(member_id):
        """
        Fetch a specific member by their ID.
        """
        member = Member.query.get(member_id)
        if not member:
            raise ValueError(f"Member with ID {member_id} not found.")
        return member

    @staticmethod
    def restore_member(member_id):
        """
        Restores a soft-deleted member by setting is_active to True.
        """
        member = Member.query.get(member_id)
        if member:
            member.is_active = True
            db.session.commit()
        return member

    @staticmethod
    def get_all_members():
        """
        Fetches all members from the database.
        :return: A list of all members.
        """
        return Member.query.all()  # Fetch all members

    @staticmethod
    def get_paginated_members(page, per_page):
        """
        Retrieves members for the specified page with a limit on per_page.
        """
        query = Member.query.paginate(page=page, per_page=per_page, error_out=False)
        return query.items, query.total  # Return members and total count
