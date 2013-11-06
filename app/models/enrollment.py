from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb

# parent = Section
class Enrollment(BasicModel):
    student_sis_id = ndb.StringProperty()
