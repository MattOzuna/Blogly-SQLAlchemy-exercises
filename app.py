"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "supersecret2224"

app.app_context().push()
connect_db(app)

@app.route('/')
def home():
    '''redirects to list of users'''
    return redirect ('/users')

@app.route('/users')
def list_users():
    '''Shows list of all users in db'''
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def create_user():
    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def submit_user():
    '''takes form data nd makes anew user'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Shows User details'''
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''allows user info to be changed'''
    user = User.query.filter_by(id=user_id).one()
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def change_user(user_id):
    '''takes form data and makes a new user'''
    user = User.query.filter_by(id=user_id).one()

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else 'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
    user.image_url = image_url
    
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''takes form data nd makes anew user'''
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect(f'/users')
