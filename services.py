from models import User, db

def addUserToDb(request_form):
    '''takes data from the create user form and adds to the database'''
    first_name = request_form['first_name']
    last_name = request_form['last_name']
    image_url = request_form['image_url']
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()

    return new_user.id

def editUserInDb(user_id, request_form):
    '''finds user in db, then changes any values and commits to db'''
    user = User.query.filter_by(id=user_id).one()

    user.first_name = request_form['first_name']
    user.last_name = request_form['last_name']

    image_url = request_form['image_url']
    image_url = image_url if image_url else 'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
    user.image_url = image_url

    db.session.commit()



