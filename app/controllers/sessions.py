from ferris.core.controller import Controller, route_with
from ferris.components.flash_messages import FlashMessages
from webapp2_extras.auth import get_auth, InvalidAuthIdError, InvalidPasswordError
import wtforms
import logging

class LoginForm(wtforms.form.Form):
    email = wtforms.fields.StringField('Email address', validators=[wtforms.validators.Email()])
    password = wtforms.fields.PasswordField('Password', validators=[wtforms.validators.Length(4, 20)])


class Sessions(Controller):
    class Meta:
        components = (FlashMessages,)
    
    @route_with('/login', methods=['GET','POST'])
    def login(self):
        form = LoginForm()
        self.parse_request(container=form)
        
        if self.request.method != 'GET' and form.validate():
            auth_id = form.email.data
            password = form.password.data
            try:
                user_dict = get_auth().get_user_by_password(auth_id, password,
                    remember=True, save_session=True)

                logging.info("Login succeeded for user %s", auth_id)
                self._flash('Login succeded!', 'success')
                
                # user_id is what our model returns in get_id method
                user_key = user_dict['user_id']
                return self.redirect(self.uri(controller='students', action='view', key=user_key))
                
            except (InvalidAuthIdError, InvalidPasswordError) as e:
                logging.info('Login failed for user %s because of %s', auth_id, type(e))
                self._flash('Login failed. Check your credentials and try again.', 'error')
                
        self.context['form'] = form
 
    @route_with('/logout', methods=['GET'])
    def logout(self):
        get_auth().unset_session()
        return self.redirect('/home/index')
        
    def _flash(self, message, mtype='info'):
        self.components.flash_messages(message, mtype)
