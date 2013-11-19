from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from app.models.teacher import Teacher
from extras.time_util import make_local_dt
import csv
import logging


# parent = Teacher
class Appointment(BasicModel):
    student_sis_id = ndb.StringProperty()
    start_time = ndb.DateTimeProperty(required=True)
    duration = ndb.IntegerProperty(required=True)
    location = ndb.StringProperty(required=True)
    teacher_name = ndb.StringProperty(required=True)
    is_active = ndb.BooleanProperty(required=True)
    is_booked = ndb.ComputedProperty(lambda self: bool(self.student_sis_id))
    
    @classmethod
    def csv_import(cls, reader):
        for row in csv.DictReader(reader):
            start_time = make_local_dt(row['date'], row['start_time'])
            teacher = Teacher.key_for_sis_id(row['teacher_sis_id'])
            appointment = cls.query(cls.start_time == start_time, ancestor=teacher).get()
            if appointment is None:
                appointment = cls(
                    parent=teacher,
                    student_sis_id = row['student_sis_id'],
                    start_time=start_time,
                    duration=row['duration'],
                    location=row['location'],
                    teacher_name=row['teacher_name'],
                    is_active=row['active']
                )
                appointment.put()
                logging.info("inserted appointment: %s" % row)
            else:
                appointment.student_sis_id = row['student_sis_id']
                appointment.start_time = start_time
                appointment.duration = row['duration']
                appointment.location = row['location']
                appointment.teacher_name = row['teacher_name']
                appointment.is_active = row['active']
                appointment.put()
                logging.info("updated appointment: %s" % row)
