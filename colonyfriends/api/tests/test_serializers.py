from django.test import TestCase

from rest_framework.serializers import ValidationError

from colonyfriends.models import Company, Person
from colonyfriends.api.serializers import PeopleInitSerializer


class PeopleInitSerializerTest(TestCase):

    def test_import_valid_data(self):

        Company.objects.create(
            id=58,
            name='fake'
        )

        payload = {
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
            "about": "Non duis dolore ad enim. Est id reprehenderit cupidatat tempor excepteur. Cupidatat labore incididunt nostrud exercitation ullamco reprehenderit dolor eiusmod sit exercitation est. Voluptate consectetur est fugiat magna do laborum sit officia aliqua magna sunt. Culpa labore dolore reprehenderit sunt qui tempor minim sint tempor in ex. Ipsum aliquip ex cillum voluptate culpa qui ullamco exercitation tempor do do non ea sit. Occaecat laboris id occaecat incididunt non cupidatat sit et aliquip.\r\n",
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
                    "index": 0
                },
                {
                    "index": 1
                },
                {
                    "index": 2
                }
            ],
            "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
            "favouriteFood": [
                "orange",
                "apple",
                "banana",
                "strawberry"
            ]
        }

        serializer = PeopleInitSerializer(data=payload)

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

    def test_validate_company_id_invalid(self):

        serializer = PeopleInitSerializer()

        self.assertRaises(
            ValidationError, serializer.validate_company_id, 888
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
