from models import User, db, Post, PostTag, Tag
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

    new_tag1 = Tag(name='Cool', posts=[new_post1, new_post2])
    new_tag2 = Tag(name='Fun')
    new_tag3 = Tag(name='Amazing')

    db.session.add_all([new_tag1, new_tag2, new_tag3])
    db.session.commit()

    
    new_post_tag1 = PostTag(post_id = new_post1.id,
                            tag_id= new_tag3.id)
    
    new_post_tag2 = PostTag(post_id = new_post2.id,
                            tag_id= new_tag2.id)
    
    
    db.session.add_all([new_post_tag1, new_post_tag2])
    db.session.commit()