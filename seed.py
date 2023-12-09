from models import User, db, Post
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()

    matt = User(first_name='Matt', last_name='Ozuna')
    db.session.add(matt)
    db.session.commit()

    new_post1 = Post(title='Test Post', content='This is a Test Post', user_id=1)
    new_post2 = Post(title='Test Post #2', content='This is another Test Post', user_id=1)

    db.session.add_all([new_post1,new_post2])
    db.session.commit()