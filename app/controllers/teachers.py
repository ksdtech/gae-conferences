from ferris.core.controller import Controller, route
from ferris.components import oauth
from google.appengine.ext import blobstore
from app.models.teacher import Teacher
from app.forms import CsvImportForm
import logging
# from apiclient.discovery import build

@scaffold
class Teachers(Controller):
    components = [oauth.OAuth]
    prefixes = ['admin']
    oauth_scopes = ['https://www.googleapis.com/auth/userinfo.profile', 
        'https://www.googleapis.com/auth/userinfo.email']
    
    @oauth.require_admin_credentials
    @scaffold
    def admin_list(self):
        pass
        
    @oauth.require_admin_credentials
    @scaffold
    def admin_add(self):
        pass

    @oauth.require_admin_credentials
    @scaffold
    def admin_view(self, id):
        pass
        
    @oauth.require_admin_credentials
    @scaffold
    def admin_edit(self, id):
        pass
        
    @oauth.require_admin_credentials
    @scaffold
    def admin_delete(self, id):
        pass

    @oauth.require_admin_credentials
    @route
    def admin_import(self):
        form = CsvImportForm()
        self.process_form_data(form)
        
        if self.request.method != 'GET' and form.validate():
            blob_key = form.file.data
            Teacher.import_csv(blobstore.BlobReader(blob_key))
            blobstore.delete(blob_key)
            return self.redirect(self.uri(action='admin_list'))

        url = blobstore.create_upload_url(
            success_path=self.uri(action='admin_import', _pass_all=True, _full=True),
            gs_bucket_name=None)
        self.set(form=form)
        self.set(upload_url=url)
