# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import unittest

from test.topydo_testcase import TopydoTest
from topydo.lib.Config import config


class ConfigTest(TopydoTest):
    def test_config01(self):
        self.assertEqual(config("test/data/config1").default_command(), 'do')

    def test_config02(self):
        self.assertNotEqual(config("").default_command(), 'do')

    def test_config03(self):
        self.assertTrue(config("test/data/config2").ignore_weekends())

    def test_config04(self):
        """ Test that value in file is overridden by parameter. """
        overrides = {
            ('topydo', 'default_command'): 'edit'
        }

        self.assertEqual(config("test/data/config1", p_overrides=overrides).default_command(), 'edit')

    def test_config09(self):
        """ Bad human readable dates switch value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").list_human_dates(),
                         bool(int(config().defaults["ls"]["human_readable_dates"])))

if __name__ == '__main__':
    unittest.main()
