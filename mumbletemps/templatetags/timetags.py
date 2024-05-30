from django import template
import datetime

register = template.Library()


def print_timestamp(timestamp):
    try:
        # Assume that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts).replace(tzinfo=datetime.timezone.utc)


register.filter(print_timestamp)
