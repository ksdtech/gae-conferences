from datetime import datetime
from pytz.gae import pytz
from settings import app_config

utc = pytz.timezone('UTC')
local_tz = pytz.timezone(app_config['timezone'])


def localize(dt):
    if not dt.tzinfo:
        dt = utc.localize(dt)
    return dt.astimezone(local_tz)

def normalize(dt):
    return dt.replace(tzinfo=local_tz).astimezone(utc).replace(tzinfo=None)

def parse_in_local_tz(s):
    return normalize(datetime.strptime(s,'%Y-%m-%d %H:%M:%S'))
