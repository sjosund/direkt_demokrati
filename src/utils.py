from datetime import datetime
import time


def str_to_timestamp(date_string):
    date_ = time.mktime(
        datetime.strptime(
            date_string,
            '%Y-%m-%d'
        ).timetuple()
    )
    return date_


def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).date()
