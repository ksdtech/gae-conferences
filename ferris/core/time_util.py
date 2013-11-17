from pytz.gae import pytz
from . import settings


def utc_tz():
    return pytz.timezone('UTC')


def local_tz():
    return pytz.timezone(settings.get('timezone')['local'])


def localize(dt, tz=None):
    if not dt.tzinfo:
        dt = utc_tz().localize(dt)
    if not tz:
        tz = local_tz()
    return dt.astimezone(tz)


def normalize(dt):
    return dt.replace(tzinfo=local_tz).astimezone(utc).replace(tzinfo=None)


def parse_in_local_tz(s):
    return normalize(datetime.strptime(s,'%Y-%m-%d %H:%M:%S'))
