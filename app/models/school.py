from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from extras.time_util import parse_in_local_tz
import logging
import csv

class School(BasicModel):
    name = ndb.StringProperty()
    sis_id = ndb.StringProperty()
    parent_access_start_time = ndb.DateTimeProperty()
    parent_access_end_time = ndb.DateTimeProperty()

    @classmethod
    def key_for_sis_id(cls, sis_id):
        return cls.query(cls.sis_id == sis_id).get(keys_only=True)

    @classmethod
    def import_csv(cls, reader):
        for row in csv.DictReader(reader):
            start_time = parse_in_local_tz(row['parent_access_start_time'])
            end_time = parse_in_local_tz(row['parent_access_end_time'])
            logging.info('start_time: %s' % start_time)
            logging.info('end_time: %s' % end_time)
            school = cls.find_by_sis_id(row['sis_id'])
            if school is None:
                school = cls(
                    name=row['name'],
                    sis_id=row['sis_id'],
                    parent_access_start_time=start_time,
                    parent_access_end_time=end_time
                )
                school.put()
                logging.info("inserted school: %s" % row)
            else:
                school.name = row['name']
                school.sis_id = row['sis_id']
                school.parent_access_start_time = start_time
                school.parent_access_end_time = end_time
                school.put()
                logging.info("updated school: %s" % row)
