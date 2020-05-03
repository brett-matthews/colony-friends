import datetime
from django.test import TestCase

from colonyfriends.models import Company, Person
from colonyfriends.services import get_common_friends


class GetCommonFriendServiceTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(id=1, name='fake')

    def test_no_people_errors(self):
        self.assertRaises(AssertionError, get_common_friends, [])

    def test_one_person_errors(self):

        person1 = Person.objects.create(
            id=1,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        self.assertRaises(AssertionError, get_common_friends, [person1])

    def test_no_common_friends(self):

        person1 = Person.objects.create(
            id=1,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person2 = Person.objects.create(
            id=2,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person3 = Person.objects.create(
            id=3,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person4 = Person.objects.create(
            id=4,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person1.friends.add(person2)
        person1.save()

        person4.friends.add(person3)
        person4.save()

        common_friends = get_common_friends([person1, person4])

        self.assertEqual(common_friends.count(), 0)

    def test_one_common_friend(self):

        person1 = Person.objects.create(
            id=1,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person2 = Person.objects.create(
            id=2,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person3 = Person.objects.create(
            id=3,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person4 = Person.objects.create(
            id=4,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        person1.friends.add(person2)
        person1.friends.add(person3)
        person1.save()

        person4.friends.add(person3)
        person4.save()

        common_friends = get_common_friends([person1, person4])

        self.assertEqual(common_friends.count(), 1)
