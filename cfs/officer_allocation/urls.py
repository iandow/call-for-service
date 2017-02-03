"""cfsbackend URL Configuration."""

from django.conf.urls import url

from officer_allocation import views

urlpatterns = [
    url(r'^api/(?P<agency_code>[A-Za-z0-9]+)/officer_allocation/',
        views.APIOfficerAllocationView.as_view(), name='officer_allocation_api'),
    url(r'^(?P<agency_code>[A-Za-z0-9]+)/officer_allocation$',
        views.OfficerAllocationDashboardView.as_view(), name='officer_allocation'),
]
