from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase



class CommandTests(TestCase):

    #  check to see if db is avaliable
    #  use patch to mock connection handler
    #  mock behaviour of get item through gi.return value = True
    def test_wait_for_db_read(self):
        """test waiting for db when db is avaliable"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    #  test, wait one sec, check again so no overload on testing connections
    # speeds up testing
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
