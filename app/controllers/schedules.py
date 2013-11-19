from ferris.components import oauth
from ferris.core import auth, scaffold
from ferris.core.controller import Controller, route
from app.helpers import csv_import
from app.models.schedule import Schedule


class Schedules(Controller):
    class Meta:
        Model = Schedule
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
    
    @route
    def admin_import(self):
        return csv_import(self)
