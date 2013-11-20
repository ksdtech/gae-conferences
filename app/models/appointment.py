from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from app.models.student import Student
from app.models.teacher import Teacher
from app.helpers import bool_from_string
from extras.time_util import make_local_dt
import csv
import logging


# parent = Teacher
class Appointment(BasicModel):
    student_id = ndb.StringProperty()
    start_time = ndb.DateTimeProperty(required=True)
    duration = ndb.IntegerProperty(required=True)
    location = ndb.StringProperty(required=True)
    teacher_name = ndb.StringProperty(required=True)
    is_active = ndb.BooleanProperty(required=True)
    is_booked = ndb.ComputedProperty(lambda self: bool(self.student_id))
    
    @classmethod
    def csv_import(cls, reader):
        for row in csv.DictReader(reader):
            teacher_id = row['teacher_id']
            student_id = row['student_id']
            start_time = make_local_dt(row['date'], row['start_time'])
            teacher = Teacher.key_for_sis_id(teacher_id)
            if teacher is None:
                logging.warn("no such teacher %s" % teacher_id)
                continue
            if student_id and Student.query(Student.sis_id == student_id).count == 0:
                logging.warn("no such student %s" % student_id)
                continue
            appointment = cls.query(cls.start_time == start_time, ancestor=teacher).get()
            if appointment is None:
                appointment = cls(
                    parent=teacher,
                    student_id=student_id,
                    start_time=start_time,
                    duration=int(row['duration']),
                    location=row['location'],
                    teacher_name=row['teacher_name'],
                    is_active=bool_from_string(row['active'])
                )
                appointment.put()
                logging.info("inserted appointment: %s" % row)
            else:
                appointment.student_id = student_id
                appointment.start_time = start_time
                appointment.duration = int(row['duration'])
                appointment.location = row['location']
                appointment.teacher_name = row['teacher_name']
                appointment.is_active = bool_from_string(row['active'])
                appointment.put()
                logging.info("updated appointment: %s" % row)
