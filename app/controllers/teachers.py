from ferris.core.controller import Controller, route
from ferris.core import scaffold
from ferris.components import oauth
from google.appengine.ext import blobstore
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
 
    class Scaffold:
        pass
    
    @oauth.require_admin_credentials
    def admin_list(self):
        pass
        
    @oauth.require_admin_credentials
    def admin_add(self):
        pass

    @oauth.require_admin_credentials
    def admin_view(self, id):
        pass
        
    @oauth.require_admin_credentials
    def admin_edit(self, id):
        pass
        
    @oauth.require_admin_credentials
    def admin_delete(self, id):
        pass

    @oauth.require_admin_credentials
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
        self.context['form'] = form
        self.context['upload_url'] = url
