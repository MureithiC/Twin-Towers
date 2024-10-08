from faker import Faker

fake = Faker()

class Member:
    members_data = []
    
    # Generate mock data
    for _ in range(100):
        members_data.append({
            "id": fake.random_int(min=1, max=1000),
            "name": fake.name(),
            "email": fake.email(),
            "isActive": fake.boolean(chance_of_getting_true=70)  # 70% chance of being active
        })

    @classmethod
    def get_active_members(cls):
        """Return only active members."""
        return [member for member in cls.members_data if member["isActive"]]
