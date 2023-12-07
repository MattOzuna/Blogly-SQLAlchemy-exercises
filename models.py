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
    first_name = db.Column(db.Text,
                         nullable=False)
    
    last_name = db.Column(db.Text,
                        nullable=False)
    
    image_url = db.Column(db.Text,
                        nullable=True,
                        default='https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png')
    
    
    