from google.appengine.ext import blobstore
from forms import CsvImportForm


def bool_from_string(s):
    if s is True or s is False:
        return s
    s = str(s).strip().lower()
    return not s in ['false','f','no','n','0','']

def csv_import(controller):
    form = CsvImportForm()
    controller.parse_request(container=form)
    
    if controller.request.method != 'GET' and form.validate():
        blob_key = form.file.data
        controller.meta.Model.csv_import(blobstore.BlobReader(blob_key))
        blobstore.delete(blob_key)
        return controller.redirect(controller.uri(action='list'))

    url = blobstore.create_upload_url(
        success_path=controller.uri(_pass_all=True, _full=True),
        gs_bucket_name=None)
    controller.context.set(**{ 'form': form, 'upload_url': url })
