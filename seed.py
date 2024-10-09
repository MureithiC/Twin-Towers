from app import create_app, db
from app.models.member import Member

def seed_database():
    """Seed the database with fake members."""
    db.create_all()

    # Generate fake members and one admin
    fake_members = Member.generate_fake_data(count=10)
    
    # Create an admin user and set a password
    admin_member = Member(name="Admin User", phone="1234567890", email="admin@example.com", role="admin", isActive=True)
    admin_member.set_password("adminpassword123")  # Set a password for the admin

    # Add admin member and fake members to the session
    db.session.add(admin_member)
    db.session.add_all(fake_members)
    
    # Commit to the database
    db.session.commit()
    
    print("Database seeded with fake data!")

if __name__ == "__main__":
    # Create app and seed database within app context
    app = create_app()
    with app.app_context():
        seed_database()
