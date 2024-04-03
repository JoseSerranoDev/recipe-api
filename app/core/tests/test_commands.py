"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Command.check is method provided by Django to check commands
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ Test commands. """

    def test_wait_for_db(self, patched_check):
        """ Test waiting for database if database ready. """

        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # Mock the sleep method to not wait the real seconds in the tests
    @patch('time.sleep')
    # The parameters have an ascendant order base on the decorator patch
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test waiting for db when geting OperationalError. """

        # The first 2 times we call the mocked method we wanna
        # raise Psycopg2Error then we raise 3 OperationalError
        # and finally we get a True value in the six time
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # we are gonna called our mocked method 6 times
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
