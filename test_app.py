from unittest import TestCase
from app import app
from models import db, User, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.app_context().push()
connect_db(app)

db.drop_all()
db.create_all()

class UserRoutesTestCase(TestCase):
    def setUp(self):

        User.query.delete()

        matt = User(first_name='Matt', last_name='Ozuna')

        db.session.add(matt)
        db.session.commit() 

        self.user_id = matt.id

    def tearDown(self):
        db.session.rollback()

    def test_redirect_users_page(self):
        with app.test_client() as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn('<h1>All Users</h1>', html)
            self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        with app.test_client() as client:
            example = {'first_name': 'test', 'last_name': 'user', 'image_url': ''}
            response = client.post("/users/new", data=example, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<li>test</li>', html)
            self.assertIn('<li>user</li>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            test={"first_name":"Test", "last_name": "user", "image_url": ''}
            response=client.post(f'/users/{self.user_id}/edit', data=test, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<li>Test</li>', html)
            self.assertIn('<li>user</li>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            response=client.post(f'/users/1/delete', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn('<h1>All Users</h1>', html)
            self.assertNotIn('<li><a href="/users/1">Matt Ozuna</a></li>', html)
            self.assertEqual(response.status_code, 200)

    



    