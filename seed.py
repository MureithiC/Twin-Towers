from faker import Faker
from app import create_app, db
from app.models.member import Member

fake = Faker()

def seed_members(count=10):
    """Seeds the database with fake Member data, including an inactive member."""
    for _ in range(count):
        member = Member(
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            role=fake.random_element(elements=("member", "admin")),
            is_active=True
        )
        
        
        member.set_password('password123')  
        
        db.session.add(member)
    

    inactive_member = Member(
        name="Inactive User",
        phone="555-555-5555",
        email="inactiveuser@example.com",
        role="member",
        is_active=False  
    )
    
    
    inactive_member.set_password('password123')
    db.session.add(inactive_member)

    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  
        seed_members(10)  

    print("Database seeded with fake member data, including an inactive member.")
