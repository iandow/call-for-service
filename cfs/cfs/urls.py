"""cfs URL Configuration."""

from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from core import views
from core.plugins import iterload

router = routers.DefaultRouter()
router.register(r'calls', views.CallViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/call_volume/$', views.APICallVolumeView.as_view()),
    url(r'^api/response_time/$', views.APICallResponseTimeView.as_view()),
    url(r'^api/call_map/', views.APICallMapView.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^(?P<agency_code>[A-Za-z0-9]+)/$', views.LandingPageView.as_view()),
    url(r'^(?P<agency_code>[A-Za-z0-9]+)/call_volume/$',
        views.CallVolumeView.as_view(), name="call_volume"),
    url(r'^(?P<agency_code>[A-Za-z0-9]+)/response_time/$',
        views.ResponseTimeView.as_view(), name="response_time"),
    url(r'^(?P<agency_code>[A-Za-z0-9]+)/calls/$', views.CallListView.as_view(),
        name="calls"),
    url(r'^(?P<agency_code>[A-Za-z0-9]+)/calls.csv$',
        views.CallExportView.as_view(), name="calls_csv"),
    url(r'^(?P<agency_code>[A-Za-z0-9]+)/call_map/$', views.MapView.as_view(),
        name="call_map")
]

for module in iterload('urls'):
    urlpatterns += module.urlpatterns
