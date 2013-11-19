from ferris.components import oauth
from ferris.core import auth, scaffold
from ferris.core.controller import Controller, route
from app.helpers import csv_import
from app.models.student import Student
from extras import db_auth


class Students(Controller):
    class Meta:
        Model = Student
        prefixes = ('admin',)
        components = (scaffold.Scaffolding, oauth.OAuth)
        oauth_scopes = ('https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email')
        authorizations = (auth.require_admin_for_prefix(prefix=('admin',)),
            db_auth.require_db_user_for_action(action=('appointments',)))
    
    admin_list   = scaffold.list
    admin_view   = scaffold.view
    admin_add    = scaffold.add
    admin_edit   = scaffold.edit
    admin_delete = scaffold.delete

    def _init_meta(self):
        super(Students, self)._init_meta()
        db_auth.add_db_user_meta(self)

    @route
    def appointments(self):
        self.context['student'] = self.db_user

    @route
    def admin_import(self):
        return csv_import(self)
