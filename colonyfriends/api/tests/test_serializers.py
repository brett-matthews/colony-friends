import datetime
from unittest.mock import patch

from django.test import TestCase

from rest_framework.serializers import ValidationError

from colonyfriends.models import Company, Person
from colonyfriends.api.serializers import (
    PeopleInitSerializer, PeopleInitListSerializer,
    FriendPostCreateSerializer
)


class FriendPostCreateSerializerTest(TestCase):

    def setUp(self):
        self.person1 = Person.objects.create(
            id=1,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.utcnow()
        )
        self.person2 = Person.objects.create(
            id=2,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.utcnow()
        )

    def test_validate_index_invalid(self):
        serializer = FriendPostCreateSerializer(data={'index': 50})
        self.assertRaises(ValidationError, serializer.validate_index, 50)

    def test_save_friend_is_self(self):
        serializer = FriendPostCreateSerializer(data={'index': 1}, context={'person': self.person1})
        serializer.is_valid()
        self.assertIsNone(serializer.save())

    def test_save_friend(self):
        serializer = FriendPostCreateSerializer(data={'index': 2}, context={'person': self.person1})
        serializer.is_valid()
        self.assertEqual(serializer.save(), 2)


class PeopleInitListSerializerTest(TestCase):

    def setUp(self):

        mock_child = patch(
            'colonyfriends.api.serializers.PeopleInitListSerializer.child'
        )
        self.mock_child = mock_child.start()
        self.addCleanup(mock_child.stop)

        mock_registered_date = patch(
            'colonyfriends.api.serializers.PeopleInitListSerializer._get_registered_date'
        )
        self.mock_registered_date = mock_registered_date.start()
        self.addCleanup(mock_registered_date.stop)

    def test__map_person_model_data(self):

        registered_date = datetime.datetime(
            year=2016, month=7, day=13,
            hour=12, minute=29, second=7,
            tzinfo=datetime.timezone(-datetime.timedelta(hours=10))
        )

        self.mock_registered_date.return_value = registered_date

        payload = {
            "index": 0,
            "balance": "$2,418.59",
            "eyeColor": "blue",
            "registered": "2016-07-13T12:29:07 -10:00",
        }

        person = PeopleInitListSerializer()._map_person_model_data(
            payload
        )

        self.assertEqual(person.id, 0)
        self.assertEqual(person.balance, "2418.59")
        self.assertEqual(person.eye_colour, "blue")
        self.assertEqual(person.registered, registered_date)


class PeopleInitSerializerTest(TestCase):

    def test_import_valid_data(self):

        Company.objects.create(
            id=58,
            name='fake'
        )

        payload = [
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

        serializer = PeopleInitSerializer(data=payload, many=True)

        serializer.is_valid()
        print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(
            Person.objects.filter(name='Carmella Lambert').count(), 1
        )

        self.assertEqual(
            Person.objects.filter(name='Carmella Lambert').first().tags.count(),
            7
        )

    def test_validate_company_id_valid(self):

        company = Company.objects.create(
            name='fake'
        )

        self.assertEqual(
            company.id,
            PeopleInitSerializer().validate_company_id(
                company.id
            ),
        )

    def test_validate_company_id_invalid_return_none(self):

        self.assertEqual(
            None,
            PeopleInitSerializer().validate_company_id(
                888
            ),
        )

    def test_validate_registered_valid(self):

        datetime_str = '2016-06-05T03:34:21 -10:00'

        self.assertEqual(
            datetime_str,
            PeopleInitSerializer().validate_registered(
                datetime_str
            ),
        )

    def test_validate_registered_invalid(self):

        datetime_str = '2016/06/05T03:34:21 -10:00'

        serializer = PeopleInitSerializer()

        self.assertRaises(
            ValidationError, serializer.validate_registered, datetime_str
        )
