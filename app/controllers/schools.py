from google.appengine.ext import blobstore
from ferris.components import oauth
from ferris.core import scaffold
from ferris.core.controller import Controller, route
from app.forms import CsvImportForm
from app.models.school import School
import logging


class Schools(Controller):
    class Meta:
        Model = School
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
        form = CsvImportForm()
        self.parse_request(container=form)
        
        if self.request.method != 'GET' and form.validate():
            blob_key = form.file.data
            School.import_csv(blobstore.BlobReader(blob_key))
            blobstore.delete(blob_key)
            return self.redirect(self.uri(action='list'))

        url = blobstore.create_upload_url(
            success_path=self.uri(_pass_all=True, _full=True),
            gs_bucket_name=None)
        self.context.set(**{ 'form': form, 'upload_url': url })
