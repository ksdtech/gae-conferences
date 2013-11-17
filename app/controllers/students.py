from ferris.core.controller import Controller, route
from ferris.components import oauth
from webapp2_extras.auth import get_auth

from google.appengine.ext import blobstore
from app.models.student import Student
from app.forms import CsvImportForm
from decorator import decorator
import logging
# from apiclient.discovery import build


@decorator
def require_user_credentials(method, handler, *args, **kwargs):
    """
    Requires that valid credentials exist for the current user before executing the handler.
    Will redirect the user for authorization.
    """
    if not get_auth().get_user_by_session():
        handler.redirect(handler.uri('login'))
    return method(handler, *args, **kwargs)    

@scaffold
class Students(Controller):
    components = [oauth.OAuth]
    prefixes = ['admin']
    oauth_scopes = ['https://www.googleapis.com/auth/userinfo.profile', 
        'https://www.googleapis.com/auth/userinfo.email']
        
    @require_user_credentials
    @scaffold
    def view(self, id):
        pass
    
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
            Student.import_csv(blobstore.BlobReader(blob_key))
            blobstore.delete(blob_key)
            return self.redirect(self.uri(action='admin_list'))

        url = blobstore.create_upload_url(
            success_path=self.uri(action='admin_import', _pass_all=True, _full=True),
            gs_bucket_name=None)
        self.set(form=form)
        self.set(upload_url=url)
