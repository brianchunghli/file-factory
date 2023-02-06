import os
import tempfile

import pytest

pytest_plugins = 'pytester'

# fixtures defines a function as an
# function parameter that we can pass
# into our tests.
# >>> in conftest.py <<
# @ pytest.fixture
# def f():
#   yield None
#
# >>> In test file <<<
# e.g., test_tests(f)


# This is automatically run thanks
# to the autouse flag
@pytest.fixture(scope='session', autouse=True)
def cleanup():
    yield None
    os.system('rm -rf test.out')


# defaults to function call
@pytest.fixture
def test_program():
    yield os.getcwd() + '/src/files.py'
