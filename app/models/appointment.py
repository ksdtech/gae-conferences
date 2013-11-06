from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb

# parent = Teacher
class Appointment(BasicModel):
    student_sis_id = ndb.StringProperty()
    start_time = ndb.DateTimeProperty()
    duration = ndb.IntegerProperty()
    location = ndb.StringProperty()
    teacher_name = ndb.StringProperty()