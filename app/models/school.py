from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from extras.time_util import make_local_dt
import csv
import logging


class School(BasicModel):
    name = ndb.StringProperty(required=True)
    sis_id = ndb.StringProperty(required=True)
    parent_access_start = ndb.DateTimeProperty(required=True)
    parent_access_end = ndb.DateTimeProperty(required=True)

    @classmethod
    def key_for_sis_id(cls, sis_id):
        return cls.query(cls.sis_id == sis_id).get(keys_only=True)

    @classmethod
    def csv_import(cls, reader):
        for row in csv.DictReader(reader):
            parent_access_start = make_local_dt(row['parent_start_date'], row['parent_start_time'])
            parent_access_end   = make_local_dt(row['parent_end_date'], row['parent_end_time'])
            logging.info('start: %s' % parent_access_start)
            logging.info('end: %s' % parent_access_end)
            school = cls.find_by_sis_id(row['sis_id'])
            if school is None:
                school = cls(
                    name=row['name'],
                    sis_id=row['sis_id'],
                    parent_access_start=parent_access_start,
                    parent_access_end=parent_access_end
                )
                school.put()
                logging.info("inserted school: %s" % row)
            else:
                school.name = row['name']
                school.sis_id = row['sis_id']
                school.parent_access_start = parent_access_start
                school.parent_access_end   = parent_access_end
                school.put()
                logging.info("updated school: %s" % row)
