import datetime
from unittest.mock import patch
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

        mock_get_common_friends = patch(
            'colonyfriends.api.views.get_common_friends'
        )
        self.mock_get_common_friends = mock_get_common_friends.start()
        self.addCleanup(mock_get_common_friends.stop)

    def test_url_exists(self):
        self.assertEqual(
            '/api/people/common-friends/', self.url
        )

    def test_get_returns_200(self):

        Person.objects.create(
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
