from ferris.components import oauth
from ferris.core import auth, scaffold
from ferris.core.controller import Controller, route
from app.helpers import csv_import
from app.models.appointment import Appointment


class Appointments(Controller):
    class Meta:
        Model = Appointment
        prefixes = ('admin',)
        components = (scaffold.Scaffolding, oauth.OAuth)
        oauth_scopes = ('https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email')
 
    admin_list   = scaffold.list
    admin_view   = scaffold.view
    admin_add    = scaffold.add
    admin_edit   = scaffold.edit
    admin_delete = scaffold.delete
    
    @route
    def admin_import(self):
        return csv_import(self)
