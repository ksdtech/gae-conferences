from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb

class Student(BasicModel):
    sis_id = ndb.StringProperty()