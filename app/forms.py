from google.appengine.ext import blobstore
import wtforms
import logging
import cgi

class SchoolsImportForm(wtforms.form.Form):
    file = wtforms.fields.FileField('CSV File', validators=[wtforms.validators.required()])
    
    def process(self, formdata=None, obj=None, **kwargs):
        super(SchoolsImportForm, self).process(formdata, obj, **kwargs)
        if formdata:
            value = formdata.get('file', None)
            if isinstance(value, cgi.FieldStorage) and 'blob-key' in value.type_options:
                info = blobstore.parse_blob_info(value)
                self.file.data = info.key()
                logging.error('CSV file uploaded, blob key is %s' % self.file.data)
            else:
                self.file.data = None
                logging.error('No file element in formdata')
