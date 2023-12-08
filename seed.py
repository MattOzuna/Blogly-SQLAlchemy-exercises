from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

matt = User(first_name='Matt', last_name='Ozuna')

db.session.add(matt)
db.session.commit()
