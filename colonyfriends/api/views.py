from django.db.models import Q

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

        eye_colour_query = Q()
        if eye_colour_filter:
            eye_colour_query = Q(eye_colour=eye_colour_filter)

        has_died_query = Q()
        if has_died_filter:
            has_died_query = Q(has_died=has_died_filter)

        first_query = people_list.pop().friends.filter(eye_colour_query & has_died_query)

        friends_intersection = []
        for p in people_list:
            friends_intersection.append(
                p.friends.filter(eye_colour_query & has_died_query)
            )

        common_friends = first_query.intersection(*friends_intersection)

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
