from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from core import models
from core.models import Agency
from core.views import ViewWithAgencies
from core.views import build_filter
from officer_allocation.filters import OfficerActivityFilterSet
from officer_allocation.summaries import OfficerActivityOverview


class APIOfficerAllocationView(APIView):
    """Powers officer allocation dashboard."""

    def get(self, request, agency_code, format=None):
        self.agency = get_object_or_404(Agency, code=agency_code)
        overview = OfficerActivityOverview(self.agency, request.GET)
        return Response(overview.to_dict())


class OfficerAllocationDashboardView(ViewWithAgencies):

    def get(self, request, agency_code, *args, **kwargs):
        filter_obj = build_filter(OfficerActivityFilterSet)

        # We want only the values of CallUnit where squad isn't null.
        # We don't want to show a bunch of bogus units for filtering.
        filter_obj['refs']['CallUnit'] = list(
            models.CallUnit.objects
            .filter(district__agency=self.agency, squad__isnull=False)
            .order_by('descr')
            .values_list('call_unit_id', 'descr'))

        return render_to_response("officer_allocation.html",
                                  self.get_context(
                                      asset_chunk="officer_allocation",
                                      form=filter_obj))
