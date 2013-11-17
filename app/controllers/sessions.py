from ferris.core.controller import Controller, route_with
from google.appengine.ext import ndb
from webapp2_extras.auth import get_auth, InvalidAuthIdError, InvalidPasswordError
from app.forms import LoginForm
from app.models.student import Student
import logging

class Sessions(Controller):
    
    @route_with('/login')
    def login(self):
        form = LoginForm()
        self.process_form_data(form)
        if self.request.method != 'GET' and form.validate():
            auth_id = form.email.data
            password = form.password.data
            try:
                user_dict = get_auth().get_user_by_password(auth_id, password,
                    remember=True, save_session=True)
                logging.info("Login succeeded for user %s", auth_id)
                
                # user_id is what our model returns in get_id method
                url_id = ':' + user_dict['user_id']
                return self.redirect(self.uri(controller='students', action='view', id=url_id))
            except (InvalidAuthIdError, InvalidPasswordError) as e:
                logging.info('Login failed for user %s because of %s', auth_id, type(e))
                self.flash('Login failed.  Check your credentials and try again.', 'error')
                
        self.context['form'] = form
 
    @route_with('/logout')
    def logout(self):
        get_auth().unset_session()
        self.redirect('/')
        
