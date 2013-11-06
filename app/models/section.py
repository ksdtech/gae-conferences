from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb

# parent = School
class Section(BasicModel):
    sis_id = ndb.StringProperty()
    teachers = ndb.StringProperty(repeated = True)
    course_name = ndb.StringProperty()
    course_number = ndb.StringProperty()
    section_number = ndb.StringProperty()
    