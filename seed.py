from faker import Faker
from app import create_app, db
from app.models.member import Member

fake = Faker()

def seed_members(count=10):
    """Seeds the database with fake Member data."""
    for _ in range(count):
        member = Member(
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            role=fake.random_element(elements=("member", "admin"))
        )
        
        # Set a default password for each member and hash it
        member.set_password('password123')  # You can choose any default password
        
        db.session.add(member)
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Ensure the tables are created before seeding
        seed_members(10)  # Seed the database with 10 fake members

    print("Database seeded with fake member data.")
