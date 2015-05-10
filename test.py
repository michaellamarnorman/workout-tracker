import os
import unittest

from flask import request
from project import app, db 
from config import basedir
from project.models import User, WorkoutA

TEST_DB = 'test.db'


class WorkoutTest(unittest.TestCase):
    ##############################
    #   setup and teardown       #
    ##############################

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass
    def login(self, username, password):
        return self.app.post(
                '/login',
                data=dict(username=username, password=password),
                follow_redirects=True
            )
    def create_user(self):
        new_user = User(name='mike', password='aaaaaa', email='a@b.com', role='user')
        db.session.add(new_user)
        db.session.commit()

    def register(self):
        return self.app.post(
                '/register',
                data=dict(
                    username='joe',
                    password='bbbbbb',
                    email='b@d.com',
                    confirm='bbbbbb'
                    ),
                follow_redirects=True
            )

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def start_workout(self):
        return self.app.post('/joe/1/home', follow_redirects=True)

    def create_finished_workout_a(self):
        pass

    def create_finished_workout_b(self):
        pass

    def create_incomplete_workout_a(self):
        pass

    def create_incomplete_workout_b(self):
        pass

    #################
    #   Test views  #
    #################
    def test_reach_homepage(self):
        response = self.app.get('/', follow_redirects=False)
        self.assertIn("Basic user", str(response.data))


    def test_can_reach_login(self):
        response = self.app.get("/login", follow_redirects=False)
        self.assertIn('Username', str(response.data))

    def test_can_reach_register(self):
        response = self.app.get("/register", follow_redirects=False)
        self.assertIn('Confirm Password', str(response.data))

    def test_users_can_login(self):
        self.register()
        response = self.login('joe', 'bbbbbb')
        self.assertIn('There are no previous stats! this is your first workout', str(response.data))

    def test_users_can_get_to_first_workout(self):
        self.register()
        self.login('joe', 'bbbbbb')
        response = self.app.get('/joe/1/workout/1/A')
        self.assertIn('Squat', str(response.data))

    def test_incorrect_login(self):
        response = self.login('abe', 'asfassfa')
        self.assertIn('Username or password was incorrect', str(response.data))

    def test_users_can_logout(self):
        self.register()
        self.login('joe', 'bbbbbb')
        response = self.logout()
        self.assertIn("Basic user", str(response.data))

    def test_same_user_cannot_register(self):
        self.register()
        response = self.register()
        self.assertIn("Username and/or email already exists.", str(response.data))

    def test_can_reach_workout(self):
        self.register()
        self.login('joe', 'bbbbbb')
        response = self.app.post("/joe/1/home", follow_redirects=True)
        #print(response.data)
        self.assertIn('Squat', str(response.data))
        self.assertIn('Bench', str(response.data))
        self.assertIn('Row', str(response.data))

    # actual app is using ajax for this test
    def test_post_workout(self):
        self.register()
        self.login('joe', 'bbbbbb')
        self.app.post('/joe/1/home', follow_redirects=True)
        response =self.app.post(
            '/save_workout/joe/1/2',
            data=dict(
                squat='5,5,5,5,5',
                bench='5,5,5,5,5',
                row="5,5,5,5,5"
            ),
            follow_redirects=True)
        self.assertIn('Workout saved', str(response.data))

    def test_next_workout_is_created(self):
        self.register()
        self.login('joe', 'bbbbbb')
        self.app.post('/joe/1/home', follow_redirects=True)
        response = self.app.post(
            '/save_workout/joe/1/2',
            data=dict(
            squat='5,5,5,5,5',
            bench='5,5,5,5,5',
            row='5,5,5,5,5'
            ),
            follow_redirects=True)
        self.assertIn('Previous Workout: \\n                A', str(response.data))
        self.assertIn('Current Workout: B', str(response.data))

    def test_can_continue_incomplete_workout(self):
        self.register()
        self.login('joe', 'bbbbbb')
        self.start_workout()
        self.app.post(
            '/write_updates/joe/1/2',
            data=dict(
                squat='5,5,5,5,5',
                bench='5,5,5,5,5',
                row='5,5,',
                follow_redirects=True
                )
            )
        response = self.app.get('/joe/1/home')
        self.assertIn('Continue Workout', str(response.data))

    def test_updates_save_from_jquery_update_view(self):
        self.register()
        self.login('joe', 'bbbbbb')
        self.start_workout()
        response = self.app.post(
            '/write_updates/joe/1/2',
            data=dict(
                squat='5,5,5,5,5',
                bench='5,5,5,5,5',
                row='5,5,',
                follow_redirects=True
                )
            )
        self.assertIn('success', str(response.data))        

if __name__=='__main__':
    unittest.main()