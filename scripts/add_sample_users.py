# Run this in a Python shell
from app import db
from models import User, Creation

# Create a user
user1 = User(
    first_name='John',
    last_name='Doe',
    email='john.doe@example.com',
    gradyear=2024,
    pronouns='he/him',
    is_admin=False
)
db.session.add(user1)

# Create another user
user2 = User(
    first_name='Jane',
    last_name='Smith',
    email='jane.smith@example.com',
    gradyear=2023,
    pronouns='she/her',
    is_admin=True
)
db.session.add(user2)
db.session.commit()

# Create a creation for user1
creation1 = Creation(
    name='My First Creation',
    caption='This is my first creation.',
    user=user1
)
db.session.add(creation1)
db.session.commit()
