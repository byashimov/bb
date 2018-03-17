import datetime

from pytz import timezone

CET = timezone('CET')
WEEKDAYS = set(range(7))


def get_next_date(dt=None, draw_weekdays=(2, 4)):
    """
    Returns the next valid draw date starting from `dt`.

    :param dt: None, date or datetime to start from
    :param draw_weekdays: Tuple of integers from 0 to 6 (Sunday)
    :return date: Date object
    """

    assert WEEKDAYS.issuperset(draw_weekdays), \
        'Invalid `draw_weekdays`, expected from 0 to 6'

    if not dt:
        dt = datetime.datetime.now(tz=CET)
    elif type(dt) is datetime.date:
        dt = datetime.datetime(dt.year, dt.month, dt.day)
    elif dt.tzinfo is None:
        dt = CET.localize(dt)
    else:
        dt = dt.astimezone(CET)

    wd = dt.weekday()
    delta_days = filter(bool, ((x - wd) % 7 for x in draw_weekdays))
    result = dt + datetime.timedelta(days=min(delta_days))

    # It said it should return "the next valid draw date"
    return result.date()
