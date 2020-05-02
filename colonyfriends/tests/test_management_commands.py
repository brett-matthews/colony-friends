import json
from unittest.mock import patch

from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class InitCompaniesTest(TestCase):

    def setUp(self):

        mock_open = patch('colonyfriends.management.commands.init_companies.open')
        self.mock_open = mock_open.start()
        self.addCleanup(mock_open.stop)

        mock_json_load = patch('colonyfriends.management.commands.init_companies.json.load')
        self.mock_json_load = mock_json_load.start()
        self.addCleanup(mock_json_load.stop)

    def test_command_success(self):

        self.mock_json_load.return_value = [{'index': 0, 'company': 'fake1'}, {'index': 1, 'company': 'fake2'}]

        out = StringIO()
        call_command('init_companies', stdout=out)
        self.assertIn('Successfully Initialised Companies', out.getvalue())

    def test_invalid_json_input(self):

        self.mock_json_load.side_effect = json.decoder.JSONDecodeError(msg='fake', doc='', pos=1)
        self.assertRaises(CommandError, call_command, 'init_companies')

    def test_command_failure_invalid_input(self):

        self.mock_json_load.return_value = [{'index': 0, 'bad_key': 'fake1'}, {'index': 1, 'bad_key': 'fake2'}]
        self.assertRaises(CommandError, call_command, 'init_companies')
