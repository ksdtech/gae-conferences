from ferris.core.controller import Controller, route
from webapp2_extras.auth import get_auth
import logging

class Home(Controller):
    @route
    def index(self):
        u = get_auth().get_user_by_session()
        logging.info("user is %s" % u)
        self.context['user'] = u
