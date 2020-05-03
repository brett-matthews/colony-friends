import json
from unittest.mock import patch

from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, TransactionTestCase

from colonyfriends.models import Food, Person


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


class InitPeopleTest(TransactionTestCase):

    def setUp(self):

        mock_open = patch('colonyfriends.management.commands.init_people.open')
        self.mock_open = mock_open.start()
        self.addCleanup(mock_open.stop)

        mock_json_load = patch('colonyfriends.management.commands.init_people.json.load')
        self.mock_json_load = mock_json_load.start()
        self.addCleanup(mock_json_load.stop)

        self.valid_payload = [
            {
                "_id": "595eeb9b96d80a5bc7afb106",
                "index": 0,
                "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
                "has_died": True,
                "balance": "$2,418.59",
                "picture": "http://placehold.it/32x32",
                "age": 61,
                "eyeColor": "blue",
                "name": "Carmella Lambert",
                "gender": "female",
                "company_id": 58,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                "about": "Non duis t et aliquip.\r\n",
                "registered": "2016-07-13T12:29:07 -10:00",
                "tags": [
                    "id",
                    "quis",
                    "ullamco",
                    "consequat",
                    "laborum",
                    "sint",
                    "velit"
                ],
                "friends": [
                    {
                        "index": 1
                    }
                ],
                "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
                "favouriteFood": [
                    "orange",
                    "apple",
                    "celery"
                ]
            },
            {
                "_id": "595eeb9b1e0d8942524c98ad",
                "index": 1,
                "guid": "b057bb65-e335-450e-b6d2-d4cc859ff6cc",
                "has_died": False,
                "balance": "$1,562.58",
                "picture": "http://placehold.it/32x32",
                "age": 60,
                "eyeColor": "brown",
                "name": "Decker Mckenzie",
                "gender": "male",
                "company_id": 98,
                "email": "deckermckenzie@earthmark.com",
                "phone": "+1 (893) 587-3311",
                "address": "492 Stockton Street, Lawrence, Guam, 4854",
                "about": "Consecteia et.\r\n",
                "registered": "2017-06-25T10:03:49 -10:00",
                "tags": [
                    "veniam",
                    "irure",
                    "mollit",
                    "sunt",
                    "amet",
                    "fugiat",
                    "ex"
                ],
                "friends": [
                    {
                        "index": 0
                    },
                    {
                        "index": 1
                    },
                ],
                "greeting": "Hello, Decker Mckenzie! You have 2 unread messages.",
                "favouriteFood": [
                    "carrot",
                    "celery"
                ]
            },
        ]

    def test_command_success(self):

        self.mock_json_load.return_value = self.valid_payload

        out = StringIO()
        call_command('init_people', stdout=out)
        self.assertIn('Successfully Initialised People', out.getvalue())

    def test_invalid_friend_index_blocks_transaction(self):

        valid_payload = self.valid_payload

        valid_payload.append({
                "_id": "595eeb9b1e0d8942524c98ad",
                "index": 2,
                "guid": "b057bb65-e335-450e-b6d2-d4cc859ff6cc",
                "has_died": False,
                "balance": "$1,562.58",
                "picture": "http://placehold.it/32x32",
                "age": 60,
                "eyeColor": "brown",
                "name": "Decker Mckenzie",
                "gender": "male",
                "company_id": 98,
                "email": "deckermckenzie@earthmark.com",
                "phone": "+1 (893) 587-3311",
                "address": "492 Stockton Street, Lawrence, Guam, 4854",
                "about": "Consecteia et.\r\n",
                "registered": "2017-06-25T10:03:49 -10:00",
                "tags": [
                    "veniam",
                    "irure",
                    "mollit",
                    "sunt",
                    "amet",
                    "fugiat",
                    "ex"
                ],
                "friends": [
                    {
                        "index": 50
                    },
                ],
                "greeting": "Hello, Decker Mckenzie! You have 2 unread messages.",
                "favouriteFood": [
                    "carrot",
                    "celery"
                ]
            }
        )

        self.mock_json_load.return_value = valid_payload

        self.assertRaises(CommandError, call_command, 'init_people')

        self.assertEqual(Person.objects.all().count(), 0)

    def test_integration_test(self):

        self.mock_json_load.return_value = self.valid_payload

        out = StringIO()
        call_command('init_people', stdout=out)

        person1 = Person.objects.get(id=1)

        self.assertEqual(
            person1.name,
            self.valid_payload[0]['name']
        )

        foods = []
        for f in person1.favourite_foods.all():
            foods.append(f.name)
        self.assertEqual(
            foods,
            self.valid_payload[0]['favouriteFood']
        )

        person2 = Person.objects.get(id=2)

        self.assertEqual(
            person2.friends.all().count(),
            1
        )

        self.assertEqual(Food.objects.all().count(), 4)
