from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel


# parent = Section
class Enrollment(BasicModel):
    student_sis_id = ndb.StringProperty()
