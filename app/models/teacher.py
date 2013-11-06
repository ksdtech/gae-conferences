from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb
from app.models.school import School
import logging
import csv

# parent = School
class Teacher(BasicModel):
    sis_id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    location = ndb.StringProperty()
    email = ndb.StringProperty()
    is_admin = ndb.BooleanProperty()
    
    @classmethod
    def import_csv(cls, reader):
        for row in csv.DictReader(reader):
            school_key = School.key_for_sis_id(row['school_id'])
            teacher = cls.find_by_sis_id(row['sis_id'])
            if teacher is None:
                teacher = cls(
                    parent=school_key,
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    sis_id=row['sis_id'],
                    location=row['location'],
                    email=row['email'],
                    is_admin=bool(int(row['admin']))
                )
                teacher.put()
                logging.info("inserted teacher: %s" % row)
            else:
                # cannot change teacher from one school to another?
                teacher.first_name = row['first_name']
                teacher.last_name = row['last_name']
                teacher.sis_id = row['sis_id']
                teacher.location = row['location']
                teacher.email = row['email']
                teacher.is_admin = bool(int(row['admin']))
                teacher.put()
                logging.info("updated teacher: %s" % row)
    