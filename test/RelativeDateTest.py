# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import date, timedelta
import unittest

from topydo.lib.RelativeDate import relative_date_to_date
from test.TopydoTest import TopydoTest

class RelativeDateTester(TopydoTest):
    def setUp(self):
        super(RelativeDateTester, self).setUp()
        self.today = date.today()
        self.tomorrow = self.today + timedelta(1)

        self.monday = self.today
        if self.monday.weekday() != 0:
            self.monday += timedelta(7 - self.today.weekday() % 7)

    def test_zero_days(self):
        result = relative_date_to_date('0d')
        self.assertEqual(result, self.today)

    def test_one_day(self):
        result = relative_date_to_date('1d')
        self.assertEqual(result, self.tomorrow)

    def test_one_week(self):
        result = relative_date_to_date('1w')
        self.assertEqual(result, date.today() + timedelta(weeks=1))

    def test_one_month(self):
        test_date = date(2015, 1, 10)
        result = relative_date_to_date('1m', test_date)
        self.assertEqual(result, date(2015, 2, 10))

    def test_one_month_ext(self):
        test_date1 = date(2015, 1, 29)
        test_date2 = date(2016, 1, 31)
        test_date3 = date(2015, 12, 31)
        test_date4 = date(2015, 7, 31)
        test_date5 = date(2015, 10, 31)

        result1 = relative_date_to_date('1m', test_date1)
        result2 = relative_date_to_date('1m', test_date2)
        result3 = relative_date_to_date('1m', test_date3)
        result4 = relative_date_to_date('1m', test_date4)
        result5 = relative_date_to_date('1m', test_date5)

        self.assertEqual(result1, date(2015, 2, 28))
        self.assertEqual(result2, date(2016, 2, 29))
        self.assertEqual(result3, date(2016, 1, 31))
        self.assertEqual(result4, date(2015, 8, 31))
        self.assertEqual(result5, date(2015, 11, 30))

    def test_one_year(self):
        test_date = date(2015, 1, 10)
        result = relative_date_to_date('1y', test_date)
        self.assertEqual(result, date(2016, 1, 10))

    def test_leap_year(self):
        test_date = date(2016, 2, 29)
        result1 = relative_date_to_date('1y', test_date)
        result2 = relative_date_to_date('4y', test_date)
        self.assertEqual(result1, date(2017, 2, 28))
        self.assertEqual(result2, date(2020, 2, 29))

    def test_zero_months(self):
        result = relative_date_to_date('0m')
        self.assertEqual(result, self.today)

    def test_zero_years(self):
        result = relative_date_to_date('0y')
        self.assertEqual(result, self.today)

    def test_garbage1(self):
        result = relative_date_to_date('0dd')
        self.assertFalse(result)

    def test_one_day_capital(self):
        result = relative_date_to_date('1D')
        self.assertEqual(result, self.tomorrow)

    def test_today1(self):
        result = relative_date_to_date('today')
        self.assertEqual(result, self.today)

    def test_today2(self):
        result = relative_date_to_date('tod')
        self.assertEqual(result, self.today)

    def test_today3(self):
        result = relative_date_to_date('today', \
            date.today() + timedelta(1))
        self.assertEqual(result, self.today)

    def test_tomorrow1(self):
        result = relative_date_to_date('Tomorrow')
        self.assertEqual(result, self.tomorrow)

    def test_tomorrow2(self):
        result = relative_date_to_date('tom')
        self.assertEqual(result, self.tomorrow)

    def test_monday1(self):
        result = relative_date_to_date('monday')
        self.assertEqual(result, self.monday)

    def test_monday2(self):
        result = relative_date_to_date('mo')
        self.assertEqual(result, self.monday)

    def test_monday3(self):
        result = relative_date_to_date('mon')
        self.assertEqual(result, self.monday)

    def test_monday4(self):
        result = relative_date_to_date('mondayy')
        self.assertFalse(result)

    def test_offset1(self):
        result = relative_date_to_date('1d', self.tomorrow)
        self.assertEqual(result, date.today() + timedelta(2))

    def test_negative_period1(self):
        result = relative_date_to_date('-1d')
        self.assertEqual(result, date.today() - timedelta(1))

    def test_negative_period2(self):
        result = relative_date_to_date('-0d')
        self.assertTrue(result, self.today)

if __name__ == '__main__':
    unittest.main()
