from django.urls import path

from colonyfriends.api.views import CompanyEmployeeListView


urlpatterns = [
    path('company/<int:company_id>/employees/', CompanyEmployeeListView.as_view(), name='company-employees'),
]