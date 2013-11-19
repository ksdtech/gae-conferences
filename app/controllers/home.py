from ferris.core.controller import Controller, route
from google.appengine.api import users
from extras import db_auth
import logging

class Home(Controller):

    def _init_meta(self):
        super(Home, self)._init_meta()
        db_auth.add_db_user_meta(self)

    @route
    def index(self):
        self.context.set(**{ 'student': self.db_user, 'teacher': self.user,
            'student_login_url': db_auth.create_login_url(self.uri('students:appointments')),
            'teacher_login_url': users.create_login_url(self.uri('teachers:appointments')) })
