import datetime
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from colonyfriends.models import Company, Person


class CompanyEmployeeListViewTest(APITestCase):

    def setUp(self):
        self.company = Company.objects.create(id=1, name='fake')
        self.person1 = Person.objects.create(
            id=1,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )
        self.company2 = Company.objects.create(id=2, name='fake')
        self.url = reverse('company-employees', args=(self.company.id,))
        self.client = APIClient()

    def test_url_exists(self):
        self.assertEqual(
            '/api/company/1/employees/', self.url
        )

    def test_get_returns_200(self):
        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_200_OK)

    def test_invalid_company_returns_404(self):
        self.assertEqual(
            self.client.get(reverse('company-employees', args=(99999,))).status_code, status.HTTP_404_NOT_FOUND
        )

    def test_company_with_no_employees(self):
        response = self.client.get(reverse('company-employees', args=(self.company2.id,)))
        self.assertEqual(response.data, [])


class PeopleCommonFriendsViewTest(APITestCase):

    def setUp(self):
        self.company = Company.objects.create(id=1, name='fake')

        self.url = reverse('people-common-friends')
        self.client = APIClient()

    def test_url_exists(self):
        self.assertEqual(
            '/api/people/common-friends/', self.url
        )

    def test_get_returns_200(self):

        person1 = Person.objects.create(
            id=1,
            has_died=False,
            balance=100.00,
            age=10,
            registered=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10))),
            company=self.company
        )

        self.assertEqual(
            self.client.get(self.url, data={'id': 1}).status_code, status.HTTP_200_OK
        )

    def test_no_id_param_returns_404(self):
        self.assertEqual(
            self.client.get(self.url).status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_get_query_set_common_friends_no_common_friends(self):

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

        response = self.client.get(self.url, data={'id': '1,4'})

        self.assertEqual(response.data['common_friends'], [])

    def test_get_query_set_common_friends_one_common_friend(self):

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

        response = self.client.get(self.url, data={'id': '1,4'})
        self.assertEqual(len(response.data['common_friends']), 1)
