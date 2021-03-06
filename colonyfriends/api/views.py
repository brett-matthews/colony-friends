from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from colonyfriends.models import Company, Person
from colonyfriends.api.serializers import (
    CompanyEmployeeModelSerializer, PeopleCommonFriendsRequestSerializer,
    PeopleCommonFriendsSerializer, PeopleModelSerializer
)
from colonyfriends.services import get_common_friends


class CompanyEmployeeListView(generics.ListAPIView):

    serializer_class = CompanyEmployeeModelSerializer

    def get_company_or_404(self):
        try:
            return Company.objects.get(pk=self.kwargs['company_id'])
        except Company.DoesNotExist:
            raise NotFound(detail='Company {} not found'.format(self.kwargs['company_id']), code=404)

    def get_queryset(self):
        return Person.objects.filter(company_id=self.kwargs['company_id'])

    def list(self, request, company_id):
        self.get_company_or_404()
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class PeopleCommonFriendsView(APIView):

    serializer_class = PeopleCommonFriendsSerializer

    def get_queryset(self):

        people_ids = self.request.query_params.get('id', None).split(",")
        eye_colour_filter = self.request.query_params.get('eye_colour', None)
        has_died_filter = self.request.query_params.get('has_died', None)

        people = Person.objects.filter(id__in=people_ids)
        people_list = list(people)

        common_friends = get_common_friends(
            people=people_list, eye_colour_filter=eye_colour_filter, has_died_filter=has_died_filter
        )

        return {'people': people, 'common_friends': common_friends}

    def get(self, request, format=None):
        serializer = PeopleCommonFriendsRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class PeopleView(generics.RetrieveAPIView):

    queryset = Person.objects.all()
    serializer_class = PeopleModelSerializer
