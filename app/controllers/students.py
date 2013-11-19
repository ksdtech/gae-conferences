from google.appengine.ext import blobstore
from ferris.components import oauth
from ferris.core import auth, scaffold
from ferris.core.controller import Controller, route
from app.forms import CsvImportForm
from app.models.student import Student
from extras import db_auth
import logging


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
        self.context.set(**{ 'form': form, 'upload_url': url })
