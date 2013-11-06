from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb

# parent = School
class Teacher(BasicModel):
    sis_id = ndb.StringProperty()