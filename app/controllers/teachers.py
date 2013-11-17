from google.appengine.api import users
from google.appengine.ext import blobstore
from ferris.components import oauth
from ferris.core import auth, scaffold
from ferris.core.controller import Controller, route
from app.models.teacher import Teacher
from app.forms import CsvImportForm
import logging
# from apiclient.discovery import build

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
        form = CsvImportForm()
        self.parse_request(container=form)
        
        if self.request.method != 'GET' and form.validate():
            blob_key = form.file.data
            Teacher.import_csv(blobstore.BlobReader(blob_key))
            blobstore.delete(blob_key)
            return self.redirect(self.uri(action='list'))

        url = blobstore.create_upload_url(
            success_path=self.uri(_pass_all=True, _full=True),
            gs_bucket_name=None)
        self.context.set(**{ 'form': form, 'upload_url': url })
