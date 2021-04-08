
import os
import sys

import django

from django.core.management import call_command


BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, 'src')
TESTS_PATH = os.path.join(BASE_DIR, 'tests')


def _set_env():
    """Установить переменные окружения"""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
    os.environ['CONFIG_PATH'] = os.path.join(TESTS_PATH, 'conf')


# TODO переписать с использованием fabric
def _call_command(command, *args, **kwargs):
    """Вызов manage-комманды"""
    sys.path.insert(0, SRC_PATH)
    os.chdir(TESTS_PATH)

    _set_env()

    django.setup()

    call_command(command, *args, **kwargs)


def run_tests():
    # _call_command('test', 'django_sql_function')
    _call_command('test', 'tests.test_project.test_app.tests')


def make_migrations():
    _call_command('makemigrations', 'test_app')


if __name__ == '__main__':
    run_tests()
    # make_migrations()
