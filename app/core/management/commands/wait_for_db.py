"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


# Fixing db race condition, you often get working with docker compose
class Command(BaseCommand):
    """ Django command to wait for database. """

    def handle(self, *args, **options):
        """ Entrypoint for command. """

        # Log a message on console
        self.stdout.write('Waiting for database....')
        db_up = False
        while db_up is False:
            try:
                # Check if the db is ready
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # Log a succesful message on console
        self.stdout.write(self.style.SUCCESS('Database available!'))
