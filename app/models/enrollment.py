from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from app.models.school import School
from app.models.student import Student
from app.models.teacher import Teacher
from app.helpers import bool_from_string
import csv
import logging


# parent = School
class Enrollment(BasicModel):
    student_id = ndb.StringProperty(required=True)
    teacher_id = ndb.StringProperty(required=True)
    course_id = ndb.StringProperty(required=True)
    section_id = ndb.StringProperty(required=True)
    period = ndb.StringProperty(required=True)
    is_homeroom = ndb.BooleanProperty(required=True)
    is_active = ndb.BooleanProperty(required=True, default=True)

    @classmethod
    def csv_import(cls, reader):
        for row in csv.DictReader(reader):
            school = School.key_for_sis_id(row['school_id'])
            student_id = row['student_id']
            if Student.query(Student.sis_id == student_id).count() == 0:
                logging.warn("no such student %s" % student_id)
                continue
            teacher_id = row['teacher_id']
            if Teacher.query(Teacher.sis_id == teacher_id).count() == 0:
                logging.warn("no such teacher %s" % teacher_id)
                continue
            enrollment = cls(
                parent=school,
                student_id=student_id,
                teacher_id=teacher_id,
                course_id=row['course_id'],
                section_id=row['section_id'],
                period=row['period'],
                is_homeroom=bool_from_string(row['homeroom']),
                is_active=True
            )
            enrollment.put()
            logging.info("inserted enrollment: %s" % row)
