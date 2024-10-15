from faker import Faker
from app import create_app, db
from app.models.member import Member

fake = Faker()

def seed_members(count=10):
    """Seeds the database with fake Member data, including an inactive member."""
    for _ in range(count):
        member_data = {
            'username': fake.user_name(),  # Ensure username is generated
            'name': fake.name(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'role': fake.random_element(elements=("member", "admin")),
            'is_active': True
        }

        # Ensure no duplicate email or phone
        if Member.query.filter_by(email=member_data['email']).first() or Member.query.filter_by(phone=member_data['phone']).first():
            continue  # Skip if the email or phone already exists

        member = Member(**member_data)
        member.set_password('password123')  # Set a default password for all members
        
        db.session.add(member)

    # Adding a known inactive member
    inactive_member_data = {
        'username': "inactiveuser",  # Ensure username is set
        'name': "Inactive User",
        'phone': "555-555-5555",
        'email': "inactiveuser@example.com",
        'role': "member",
        'is_active': False
    }

    if not Member.query.filter_by(email=inactive_member_data['email']).first():
        inactive_member = Member(**inactive_member_data)
        inactive_member.set_password('password123')  # Set a default password for inactive member
        db.session.add(inactive_member)

    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Ensure tables are created
        seed_members(10)  # Seed the database with 10 members

    print("Database seeded with fake member data, including an inactive member.")
