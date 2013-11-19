from ferris.core.time_util import local_tz, utc_tz
from datetime import datetime
from time import time


def normalize(dt):
    return dt.astimezone(utc_tz()).replace(tzinfo=None)


# TODO: next two functions are pretty much the same
# Deal with :%S or not depending on string submitted
def parse_local_dt(s):
    tt = time.strptime(s, '%Y-%m-%d %H:%M:%S')[0:6]
    return normalize(datetime(tt[0], tt[1], tt[2], tt[3], tt[4], tt[5], 0, local_tz()))


def make_local_dt(s_date, s_time):
    year, month, day = s_date.split('-')
    hour, minute = s_time.split(':')
    return normalize(datetime(int(year), int(month), int(day), int(hour), int(minute), 0, 0, local_tz()))


def hour_and_minute_to_s(hour, minute):
    am_pm = 'am'
    if hour >= 12:
        am_pm = 'pm'
        hour -= 12
    if hour == 0:
        hour = 12
    return "%d:%02d %s" % (hour, minute, am_pm)


