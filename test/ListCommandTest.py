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

from six import u
import codecs
import re
import sys
import unittest

from topydo.lib.Config import config
from topydo.commands.ListCommand import ListCommand
from test.CommandTest import CommandTest
from test.TestFacilities import load_file_to_todolist

class ListCommandTest(CommandTest):
    def setUp(self):
        super(ListCommandTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

    def test_list1(self):
        command = ListCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list3(self):
        command = ListCommand(["Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list4(self):
        command = ListCommand(["-x", "Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list5(self):
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n|  6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list6(self):
        command = ListCommand(["Project3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_list7(self):
        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list8(self):
        command = ListCommand(["--", "-project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list9(self):
        command = ListCommand(["--", "-project1", "-Drink"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list10(self):
        command = ListCommand(["text1", "2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list11(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list12(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["-x", "project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list13(self):
        command = ListCommand(["-x", "--", "-@Context1 +Project2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list14(self):
        config("test/data/listcommand2.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, " |  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n |  4| (C) Drink beer @ home\n |  5| (C) 13 + 29 = 42\n |  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list15(self):
        command = ListCommand(["p:<10"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list16(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|t5c| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|wa5| (C) Drink beer @ home\n|z63| (C) 13 + 29 = 42\n|mfg| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list17(self):
        command = ListCommand(["-x", "id:"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n")
        self.assertEqual(self.errors, "")

    def test_list18(self):
        command = ListCommand(["-x", "date:2014-12-12"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  6| x 2014-12-12 Completed but with date:2014-12-12\n")

    def test_list19(self):
        """ Force showing all tags. """
        config('test/data/listcommand-tags.conf')

        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| (C) Baz @Context1 +Project1 key:value id:1\n|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list20(self):
        command = ListCommand(["-f text"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list21(self):
        command = ListCommand(["-f invalid"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list22(self):
        """ Handle tag lists with spaces and punctuation."""
        config(p_overrides={('ls', 'hide_tags'): 'p, id'})
        self.todolist = load_file_to_todolist('test/data/ListCommandTagTest.txt')

        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, '|  1| Foo.\n')

    def test_help(self):
        command = ListCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n\n" + command.help() + "\n")

class ListCommandUnicodeTest(CommandTest):
    def setUp(self):
        super(ListCommandUnicodeTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

    def test_list_unicode1(self):
        """ Unicode filters """
        command = ListCommand([u("\u25c4")], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())

        expected = u("|  1| (C) And some sp\u00e9cial tag:\u25c4\n")

        self.assertEqual(self.output, expected)

class ListCommandJsonTest(CommandTest):
    def test_json(self):
        todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

        command = ListCommand(["-f", "json"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.is_dirty())

        jsontext = ""
        with codecs.open('test/data/ListCommandTest.json', 'r', encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, jsontext)
        self.assertEqual(self.errors, "")

    def test_json_unicode(self):
        todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

        command = ListCommand(["-f", "json"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.is_dirty())

        jsontext = ""
        with codecs.open('test/data/ListCommandUnicodeTest.json', 'r', encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, jsontext)
        self.assertEqual(self.errors, "")

def replace_ical_tags(p_text):
    # replace identifiers with dots, since they're random.
    result = re.sub(r'\bical:....\b', 'ical:....', p_text)
    result = re.sub(r'\bUID:....\b', 'UID:....', result)

    return result

IS_PYTHON_32 = (sys.version_info.major, sys.version_info.minor) == (3, 2)

class ListCommandIcalTest(CommandTest):
    def setUp(self):
        self.maxDiff = None

    @unittest.skipIf(IS_PYTHON_32, "icalendar is not supported for Python 3.2")
    def test_ical(self):
        todolist = load_file_to_todolist("test/data/ListCommandIcalTest.txt")

        command = ListCommand(["-x", "-f", "ical"], todolist, self.out, self.error)
        command.execute()

        self.assertTrue(todolist.is_dirty())

        icaltext = ""
        with codecs.open('test/data/ListCommandTest.ics', 'r', encoding='utf-8') as ical:
            icaltext = ical.read()

        self.assertEqual(replace_ical_tags(self.output), replace_ical_tags(icaltext))
        self.assertEqual(self.errors, "")

    @unittest.skipUnless(IS_PYTHON_32, "icalendar is not supported for Python 3.2")
    def test_ical_python32(self):
        """
        Test case for Python 3.2 where icalendar is not supported.
        """
        todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

        command = ListCommand(["-f", "ical"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.is_dirty())
        self.assertEqual(self.output, '')
        self.assertEqual(self.errors, "icalendar is not supported in this Python version.\n")

    @unittest.skipIf(IS_PYTHON_32, "icalendar is not supported for Python 3.2")
    def test_ical_unicode(self):
        todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

        command = ListCommand(["-f", "ical"], todolist, self.out, self.error)
        command.execute()

        self.assertTrue(todolist.is_dirty())

        icaltext = ""
        with codecs.open('test/data/ListCommandUnicodeTest.ics', 'r', encoding='utf-8') as ical:
            icaltext = ical.read()

        self.assertEqual(replace_ical_tags(self.output), replace_ical_tags(icaltext))
        self.assertEqual(self.errors, "")

if __name__ == '__main__':
    unittest.main()
