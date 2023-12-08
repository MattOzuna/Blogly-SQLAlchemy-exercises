from models import User, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()

    matt = User(first_name='Matt', last_name='Ozuna')

    db.session.add(matt)
    db.session.commit()