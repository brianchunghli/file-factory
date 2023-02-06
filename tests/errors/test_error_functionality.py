#!/usr/bin/env python3
import os
import tempfile


def test_missing_file(test_program, pytester):
    data = pytester.run(test_program, 'make', 'test.cpp')
    data.stdout.fnmatch_lines(
        "files.py: 'test.cpp' cannot be found in current directory\n")


def test_invalid_file(test_program, pytester):
    data = pytester.run(test_program, 'make', 'test.py')
    data.stdout.fnmatch_lines("files.py: invalid file 'test.py'\n")


def test_extraneous_suffix(test_program, pytester):
    data = pytester.run(test_program, 'py', 'test.py')
    data.stdout.fnmatch_lines("files.py: extraneous suffix 'py'\n")
