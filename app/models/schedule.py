from google.appengine.ext import ndb
from ferris.core.ndb import BasicModel
from extras.time_util import hour_and_minute_to_s
from datetime import datetime
import csv
import time
import logging


def valid_hour(prop, value):
    if value < 0 or value > 23:
        raise ValueError, "hour must be between 0 and 23"

def valid_minute(prop, value):
    if value < 0 or value > 59:
        raise ValueError, "minute must be between 0 and 59"

def valid_duration(prop, value):
    if value <= 0 or value > 480:
        raise ValueError, "duration must be between 1 and 480"


class Schedule(BasicModel):
    title = ndb.ComputedProperty(lambda self: self.generate_name())
    timestamp = ndb.ComputedProperty(lambda self: self.generate_timestamp())
    date = ndb.DateProperty(required=True)
    start_time_hour = ndb.IntegerProperty(required=True, validator=valid_hour)
    start_time_minute = ndb.IntegerProperty(required=True, validator=valid_minute)
    end_time_hour = ndb.IntegerProperty(required=True, validator=valid_hour)
    end_time_minute = ndb.IntegerProperty(required=True, validator=valid_minute)
    slot_duration = ndb.IntegerProperty(required=True, validator=valid_duration)
    slot_interval = ndb.IntegerProperty(required=True, validator=valid_duration)
    is_active = ndb.BooleanProperty(required=True, default=True)
    
    def start_time_to_s(self):
        return hour_and_minute_to_s(self.start_time_hour, self.start_time_minute)

    def end_time_to_s(self):
        return hour_and_minute_to_s(self.end_time_hour, self.end_time_minute)
    
    def before_put(self):
        if self.end_time_hour < self.start_time_hour or (
            self.end_time_hour == self.start_time_hour and self.end_time_minute <= self.start_time_minute):
            raise ValueError, "end_time must be later than start time"
        if self.slot_interval < self.slot_duration:
            raise ValueError, "duration must be non-zero and interval must be at least duration"
            
    def generate_name(self):
        return "%s at %s (%d mins)" % (
            self.date.strftime('%a %b %d, %Y'), self.start_time_to_s(), self.slot_duration)
        
    def generate_timestamp(self):
        tt = self.date.timetuple()
        return int(time.mktime((tt[0], tt[1], tt[2], 
            self.start_time_hour, self.start_time_minute, 
            tt[5], tt[6], tt[7], tt[8])))
    
    @classmethod
    def csv_import(cls, reader):
        for row in csv.DictReader(reader):
            s_hour, s_min = row['start_time'].split(':')
            e_hour, e_min = row['end_time'].split(':')
            schedule = cls(
                date=datetime.strptime(row['date'], '%Y-%m-%d'),
                start_time_hour=int(s_hour),
                start_time_minute=int(s_min),
                end_time_hour=int(e_hour),
                end_time_minute=int(e_min),
                slot_duration=int(row['duration']),
                slot_interval=int(row['interval']),
                is_active=True
            )
            schedule.put()
            logging.info("inserted schedule: %s" % row)
