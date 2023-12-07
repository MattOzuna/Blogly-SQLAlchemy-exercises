from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# User.query.delete()

#add me as first user
# me = User(
#         first_name='Matt',
#         last_name='Ozuna')

#Add me to session
# db.session.add(me)

#Commit to db
# db.session.commit