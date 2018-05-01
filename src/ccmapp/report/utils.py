from collections import namedtuple


def time_para_to_days(time_range):
    if time_range == 'last_month':
        days = 30
    elif time_range == 'last_week':
        days = 7
    elif time_range == 'last_day':
        days = 1
    else:
        raise Exception('Unknown time_range: %s' % time_range)
    return days


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
