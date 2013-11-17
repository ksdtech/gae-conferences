from ferris.core.controller import Controller, route
import db_auth
import logging

class Home(Controller):

    def _init_meta(self):
        super(Home, self)._init_meta()
        db_auth.init_meta(self)

    @route
    def index(self):
        self.context.set(**{ 'student': self.db_user, 'teacher': self.user })
