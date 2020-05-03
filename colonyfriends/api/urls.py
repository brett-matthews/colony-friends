from django.urls import path

from colonyfriends.api.views import CompanyEmployeeListView, PeopleCommonFriendsView


urlpatterns = [
    path('company/<int:company_id>/employees/', CompanyEmployeeListView.as_view(), name='company-employees'),
    path('people/common-friends/', PeopleCommonFriendsView.as_view(), name='people-common-friends'),
]