from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from app.models.school import School
import csv
import logging


# parent = School
class Teacher(BasicModel):
    sis_id = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    is_admin = ndb.BooleanProperty(required=True, default=False)
    
    @classmethod
    def key_for_sis_id(cls, sis_id):
        return cls.query(cls.sis_id == sis_id).get(keys_only=True)

    @classmethod
    def csv_import(cls, reader):
        for row in csv.DictReader(reader):
            school = School.key_for_sis_id(row['school_id'])
            teacher = cls.query(cls.sis_id == row['sis_id'], ancestor=school).get()
            if teacher is None:
                teacher = cls(
                    parent=school,
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
    