from ferris.core.controller import Controller, route
from ferris.core import scaffold
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


class Students(Controller):
    class Meta:
        Model = Student
        prefixes = ('admin',)
        components = (scaffold.Scaffolding, oauth.OAuth)
        oauth_scopes = ('https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email')
        
    @require_user_credentials
    def view(self, id):
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
            Student.import_csv(blobstore.BlobReader(blob_key))
            blobstore.delete(blob_key)
            return self.redirect(self.uri(action='list'))

        url = blobstore.create_upload_url(
            success_path=self.uri(_pass_all=True, _full=True),
            gs_bucket_name=None)
        self.context['form'] = form
        self.context['upload_url'] = url
