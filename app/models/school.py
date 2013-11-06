from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb
import logging
import csv

class School(BasicModel):
    name = ndb.StringProperty()
    sis_id = ndb.StringProperty()
    parent_access_start_time = ndb.DateTimeProperty()
    parent_access_end_time = ndb.DateTimeProperty()

    @classmethod
    def import_csv(cls, reader):
        for row in csv.DictReader(reader):
            logging.error("row: %s" % row)
            
