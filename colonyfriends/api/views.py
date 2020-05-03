from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from colonyfriends.models import Company, Person
from colonyfriends.api.serializers import CompanyEmployeeModelSerializer


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
