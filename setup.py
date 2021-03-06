from setuptools import setup, find_packages
import os
import re
import codecs
import sys

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


conditional_dependencies = {
    "colorama>=0.2.5": "win32" in sys.platform,
}


setup(
    name = "topydo",
    packages = find_packages(exclude=["test"]),
    version = find_version('topydo', 'lib', 'Version.py'),
    description = "A command-line todo list application using the todo.txt format.",
    author = "Bram Schoenmakers",
    author_email = "me@bramschoenmakers.nl",
    url = "https://github.com/bram85/topydo",
    install_requires = [
        'six >= 1.9.0',
    ] + [p for p, cond in conditional_dependencies.items() if cond],
    extras_require = {
        'ical': ['icalendar'],
        'prompt-toolkit': ['prompt-toolkit >= 0.53'],
        'edit-cmd-tests': ['mock'],
    },
    entry_points= {
        'console_scripts': ['topydo = topydo.cli.UILoader:main'],
    },
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ],
    long_description = """\
topydo is a todo list application using the todo.txt format. It is heavily inspired by the todo.txt CLI by Gina Trapani. This tool is actually a merge between the todo.txt CLI and a number of extensions that I wrote on top of the CLI. These extensions are:

* Set due and start dates;
* Custom sorting;
* Dealing with tags;
* Maintain dependencies between todo items;
* Allow todos to recur;
* Some conveniences when adding new items (e.g. adding creation date and use relative dates)
""",

    test_suite = "test",
)
