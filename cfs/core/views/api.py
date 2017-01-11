from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from url_filter.integrations.drf import DjangoFilterBackend

from .. import serializers
from ..filters import CallFilterSet
from ..models import Call, Agency
from ..summaries import CallResponseTimeOverview, \
    CallVolumeOverview, CallMapOverview


class CallPagination(PageNumberPagination):
    page_size = 50


class AgencyMixin:

    def dispatch(self, request, agency_code, *args, **kwargs):
        self.agency = get_object_or_404(Agency, code=agency_code)
        return super().dispatch(request, *args, **kwargs)


class CallViewSet(AgencyMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows calls to be viewed.
    """

    serializer_class = serializers.CallSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = CallFilterSet
    pagination_class = CallPagination

    def get_queryset(self):
        return Call.objects \
            .filter(agency=self.agency) \
            .order_by('time_received') \
            .select_related('district') \
            .select_related('beat') \
            .select_related('city') \
            .select_related('priority') \
            .select_related('call_source') \
            .select_related('nature') \
            .select_related('nature__nature_group') \
            .select_related('close_code') \
            .select_related('primary_unit') \
            .select_related('first_dispatched') \
            .select_related('reporting_unit')


class APICallResponseTimeView(AgencyMixin, APIView):
    """Powers response time dashboard."""

    def get(self, request, format=None):
        overview = CallResponseTimeOverview(self.agency, filters=request.GET)
        return Response(overview.to_dict())


class APICallVolumeView(AgencyMixin, APIView):
    """Powers call volume dashboard."""

    def get(self, request, format=None):
        overview = CallVolumeOverview(self.agency, filters=request.GET)
        return Response(overview.to_dict())


class APICallMapView(AgencyMixin, APIView):

    def get(self, request, format=None):
        overview = CallMapOverview(self.agency, filters=request.GET)
        return Response(overview.to_dict())
