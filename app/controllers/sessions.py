from ferris.components.flash_messages import FlashMessages
from ferris.core import settings
from ferris.core.controller import Controller, route_with
from webapp2_extras.auth import get_auth, InvalidAuthIdError, InvalidPasswordError
import wtforms
import logging

class LoginForm(wtforms.form.Form):
    email = wtforms.fields.StringField('Email address', validators=[wtforms.validators.Email()])
    password = wtforms.fields.PasswordField('Password', validators=[wtforms.validators.Length(4, 20)])
    next = wtforms.fields.StringField(widget=wtforms.widgets.HiddenInput())

class Sessions(Controller):
    class Meta:
        components = (FlashMessages,)
    
    @route_with('/login', methods=['GET','POST'])
    def login(self):
        form = LoginForm()
        self.parse_request(container=form)
        
        if self.request.method != 'GET' and form.validate():
            email = str(form.email.data)
            password = str(form.password.data)
            try:
                db_user = get_auth().get_user_by_password(email, password,
                    remember=True, save_session=True)

                logging.info("Login succeeded for user %s", email)
                self._flash('Login succeded!', 'success')
                
                next = str(form.next.data)
                if not next:
                    next = settings.get('db_login')['login_dest_url']
                return self.redirect(next)
                
            except (InvalidAuthIdError, InvalidPasswordError) as e:
                logging.info('Login failed for user %s because of %s', email, type(e))
                self._flash('Login failed. Check your credentials and try again.', 'error')
                
        self.context['form'] = form
 
    @route_with('/logout', methods=['GET'])
    def logout(self):
        get_auth().unset_session()
        
        next = self.request.params.get('next', None)
        if not next:
            next = settings.get('db_login')['logout_dest_url']
        return self.redirect(next)
        
    def _flash(self, message, mtype='info'):
        self.components.flash_messages(message, mtype)
