from ferris.components import oauth
from ferris.core import auth, scaffold
from ferris.core.controller import Controller, route
from app.helpers import csv_import
from app.models.teacher import Teacher


class Teachers(Controller):
    class Meta:
        Model = Teacher
        prefixes = ('admin',)
        components = (scaffold.Scaffolding, oauth.OAuth)
        oauth_scopes = ('https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email')
        authorizations = (auth.require_admin_for_prefix(prefix=('admin',)),
            auth.require_user_for_action(action=('appointments',)))
 
    admin_list   = scaffold.list
    admin_view   = scaffold.view
    admin_add    = scaffold.add
    admin_edit   = scaffold.edit
    admin_delete = scaffold.delete
    
    @route
    def appointments(self):
        logout_url = users.create_logout_url('/home/index')
        self.context.set(**{ 'teacher': self.user, 'logout_url': logout_url })

    @route
    def admin_import(self):
        return csv_import(self)
