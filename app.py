"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, User, Post, PostTag, Tag
from services import addUserToDb, editUserInDb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "supersecret2224"

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
    '''takes form data and makes a new user'''
    new_user_id = addUserToDb(request.form)
    return redirect(f'/users/{new_user_id}')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Shows User details'''
    user = User.query.filter_by(id = user_id).one()
    posts = Post.query.filter_by(user_id = user_id).all()
    return render_template('user_detail.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''allows user info to be changed'''
    user = User.query.filter_by(id=user_id).one()
    return render_template('edit_user.html', user = user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def change_user(user_id):
    '''takes form data and makes a new user'''
    editUserInDb(user_id, request.form)
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''takes user id and deletes from database before redirecting back to home page'''
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(f'/users')

# =================Part 2===================================================================================== #

@app.route('/users/<int:user_id>/posts/new')
def create_post(user_id):
    '''form for new posts'''
    user = User.query.filter_by(id=user_id).one()
    return render_template('create_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    '''takes post form data and adds to the database'''
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''shows post'''
    post = Post.query.filter_by(id=post_id).one()
    user = User.query.filter_by(id=post.user_id).one()
    tags = db.session.query(Tag,PostTag).join(PostTag).filter_by(post_id=post.id).all()
    return render_template('show_post.html', post=post, user=user, tags=tags)


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''deletes post from db and send the user back to that post's user page'''
    post=Post.query.filter_by(id=post_id).one()
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''shows for for editing the original post'''
    post = Post.query.filter_by(id=post_id).one()
    return render_template(f'edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def change_post(post_id):
    '''if there are edits to the post, updates the post and submits to the db'''
    post = Post.query.filter_by(id=post_id).one()
    post.title = request.form['title'] if request.form['title'] else post.title
    post.content = request.form['content'] if request.form['content'] else post.content

    db.session.commit()
    return redirect(f'/users/{post.user_id}')

# =================Part 3===================================================================================== #

@app.route('/tags')
def all_tags():
    '''shows list of all available tags'''
    tags = db.session.query(Tag).all()
    return render_template('show_tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = db.session.query(Tag).filter_by(id=tag_id).one()
    posts = db.session.query(Post, PostTag).join(PostTag).filter_by(tag_id=tag_id).all()
    return render_template('show_tag.html', tag=tag, posts=posts)


@app.route('/tags/new', methods=['POST'])
def add_tag():
    new_tag = Tag(name=request.form['name'])
    db.session.add(new_tag)
    db.session.commit()
    return redirect ('/tags')

@app.route('/tags/new')
def new_tag():
    return render_template('create_tag.html')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = db.session.query(Tag).filter_by(id=tag_id).one()
    return render_template ('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POSTS'])
def change_tag(tag_id):
    tag = db.session.query(Tag).filter_by(id=tag_id).one()
    tag.name = request.form['name'] if request.form['name'] else tag.name
    db.session.commit()
    return redirect(f'/tags/{tag.id}')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''take the post request from the edit tag form and deletes it from the PostTag and Tag tables'''
    db.session.query(PostTag).filter_by(tag_id=tag_id).delete()
    db.session.query(Tag).filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect('/tags')

