from ferris.core.controller import Controller, route
from ferris.core import auth, scaffold
from ferris.components import oauth
from webapp2_extras.auth import get_auth
from google.appengine.ext import blobstore
from app.models.student import Student
from app.forms import CsvImportForm
from decorator import decorator
import db_auth
import logging


class Students(Controller):
    class Meta:
        Model = Student
        prefixes = ('admin',)
        components = (scaffold.Scaffolding, oauth.OAuth)
        oauth_scopes = ('https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email')
        authorizations = (auth.require_admin_for_prefix(prefix=('admin',)),
            db_auth.require_db_user)
    
    admin_list   = scaffold.list
    admin_view   = scaffold.view
    admin_add    = scaffold.add
    admin_edit   = scaffold.edit
    admin_delete = scaffold.delete

    def _init_meta(self):
        super(Students, self)._init_meta()
        db_user = get_auth().get_user_by_session()
        if db_user and db_user['user_id']:
            auth_key = self.util.decode_key(db_user['user_id'])
            self.db_user = auth_key.get()
        
    def view(self, key):
        # we ignore key (or check its validity)
        auth_key = self.db_user.key
        qs_key = self.util.decode_key(key)
        logging.info("Students.view key is %s, qs_key is %s" % (auth_key, qs_key))
        item = auth_key.get()
        if not self.db_user:
            return 404
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
