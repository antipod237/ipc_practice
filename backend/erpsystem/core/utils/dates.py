import re
import datetime
from pytz import utc


def convert_to_utc(dt):
    """Return same datetime if it's aware or sets it's timezone to UTC."""

    if dt is None:
        dt = datetime.datetime.utcfromtimestamp(0)

    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return dt.replace(tzinfo=utc)

    return dt


def get_date(text_date):
    if re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', text_date):
        year, month, day = [int(i) for i in text_date.split('-')]
        return datetime.date(year, month, day)
    raise ValueError
