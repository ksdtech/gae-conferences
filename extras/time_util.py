from ferris.core.time_util import local_tz, utc_tz

def normalize(dt):
    return dt.replace(tzinfo=local_tz()).astimezone(utc_tz()).replace(tzinfo=None)

def parse_in_local_tz(s):
    return normalize(datetime.strptime(s,'%Y-%m-%d %H:%M:%S'))
