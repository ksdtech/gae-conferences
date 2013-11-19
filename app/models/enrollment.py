from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from app.models.school import School
import csv
import logging


# parent = School
class Enrollment(BasicModel):
    student_sis_id = ndb.StringProperty(required=True)
    teacher_sis_id = ndb.StringProperty(required=True)
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
            teacher_id = row['teacher_id']
            enrollment = cls(
                parent=school,
                student_sis_id=student_id,
                teacher_sis_id=teacher_id,
                course_id=row['course_id'],
                section_id=row['section_id'],
                period=row['period'],
                is_homeroom=bool(row['homeroom']),
                is_active=True
            )
            enrollment.put()
            logging.info("inserted enrollment: %s" % row)
