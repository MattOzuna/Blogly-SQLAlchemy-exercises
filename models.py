import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String,
                         nullable=False)
    
    last_name = db.Column(db.String,
                        nullable=False)
    
    image_url = db.Column(db.String,
                        nullable=True,
                        default='https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png')
    
    def __repr__(self):
        return f"<id: {self.id} Name:{self.first_name} {self.last_name} >"
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text,
                         nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts', lazy='subquery')

    

    def __repr__(self):
        return f"<Post id: {self.id}, User id: {self.user_id}, Title:{self.title}, Content:{self.content}, Created at: {self.created_at} >"
    

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    
    posts = db.relationship('Post',
                           secondary='post_tag',
                           backref='tags',
                           lazy=True)
    
    
class PostTag(db.Model):
    __tablename__ = 'post_tag'

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.id"),
                        primary_key=True)
    
    
    
    