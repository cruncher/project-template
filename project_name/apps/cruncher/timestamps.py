import datetime
import pytz


def to_timestamp(dt):
    # Ref: http://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
    if dt is None:
        return None

    td = dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
    return int(((td.seconds + td.days * 24 * 3600) * 10 ** 6) / 1e6)


def from_timestamp(ts):
    return datetime.datetime.fromtimestamp(float(ts), tz=pytz.utc)
