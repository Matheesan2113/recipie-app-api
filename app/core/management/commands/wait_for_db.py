import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    """Django ommand to pause execution until db is avaliable"""

    # Wait for db connection

    def handle(self, *args, **options):
        self.stdout.write('waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Databse unavliable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database avaliable!'))
