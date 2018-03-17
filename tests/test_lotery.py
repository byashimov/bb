from datetime import date, datetime
from functools import partial

from freezegun import freeze_time
from pytz import UTC, timezone
from unittest2 import TestCase

from bb.lotery import CET, get_next_date


class GetNextDateTestCase(TestCase):
    def test_before_or_equal_cet(self):
        timezones = (UTC, CET, None)

        cases = (
            ((2018, 3, 17), date(2018, 3, 21)),  # Sat => Wed
            ((2018, 3, 16), date(2018, 3, 21)),  # Fri => Wed
            ((2018, 3, 21), date(2018, 3, 23)),  # Wed => Fri
            ((2018, 3, 23), date(2018, 3, 28)),  # Fri => Wed
            ((2018, 4, 2), date(2018, 4, 4)),  # Mon => Wed

            # Dst in Ireland, forward from 1 to 2 am
            ((2018, 3, 25, 1, 30), date(2018, 3, 28)),  # Sun => Wed
        )

        for tz in timezones:
            for args, expected in cases:
                with self.subTest(tz=tz, args=args, expected=expected):
                    from_date = datetime(*args, tzinfo=tz)
                    self.assertEqual(get_next_date(from_date), expected)

    def test_after_cet(self):
        moscow = partial(datetime, tzinfo=timezone('Europe/Moscow'))
        cases = (
            ((2018, 3, 17), date(2018, 3, 21)),  # Sat => Wed
            ((2018, 3, 16), date(2018, 3, 16)),  # Fri => Wed
            ((2018, 3, 21), date(2018, 3, 21)),  # Wed => Fri
            ((2018, 3, 23), date(2018, 3, 23)),  # Fri => Wed
            ((2018, 4, 2), date(2018, 4, 4)),  # Mon => Wed

            # Dst in Ireland, forward from 1 to 2 am
            ((2018, 3, 25, 1, 30), date(2018, 3, 28)),  # Sun => Wed
        )

        for args, expected in cases:
            with self.subTest(args=args, expected=expected):
                from_date = moscow(*args)
                self.assertEqual(get_next_date(from_date), expected)

    def test_iso_week_days(self):
        with self.assertRaises(AssertionError) as e:
            get_next_date(draw_weekdays=[7])
        self.assertEqual(
            'Invalid `draw_weekdays`, expected from 0 to 6',
            e.exception.message
        )

    @freeze_time('2018-03-16', tz_offset=0)
    def test_default_datetime_is_today(self):
        today = date.today()
        expected = date(2018, 3, 21)

        # Equal result
        self.assertEqual(get_next_date(), expected)
        self.assertEqual(get_next_date(today), expected)

    def test_date_instance(self):
        self.assertEqual(get_next_date(date(2018, 3, 16)), date(2018, 3, 21))
