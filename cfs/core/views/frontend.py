import itertools
import csv
from io import StringIO

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic import View
from url_filter.filtersets import StrictMode

from core import models
from core.models import Call, Agency
from core.serializers import CallExportSerializer
from ..filters import CallFilterSet


def build_filter(filter_set):
    fields = filter_set.definition
    out = {"fields": [f for f in fields if not f['name'] == 'call']}
    refs = {}

    for field in fields:
        if field.get('rel') and not refs.get(field['rel']):
            # Enabling filtering on related fields will be tricky for
            # the Call model, since it's not just a descr we need to
            # display.  We'll bypass that for now.
            if field['rel'] == 'Call':
                continue

            model = getattr(models, field['rel'])
            pk_name = model._meta.pk.name
            refs[field['rel']] = list(
                model.objects.all().order_by("descr").values_list(pk_name,
                                                                  "descr"))

    out["refs"] = refs
    return out


class LandingPageView(View):

    def get(self, request):
        agencies = Agency.objects.all()
        if len(agencies) == 1:
            return redirect(
                reverse('agency', kwargs={"agency_code": agencies[0].code}))
        else:
            return render_to_response('agency_list.html',
                                      {"agencies": agencies,
                                       "agency": agencies[0]})
            pass  # render


class ViewWithAgencies(View):

    def dispatch(self, request, *args, **kwargs):
        agency_code = kwargs['agency_code']
        self.agency = get_object_or_404(Agency, code=agency_code)
        return super().dispatch(request, *args, **kwargs)


class AgencyLandingPageView(ViewWithAgencies):

    def get(self, request, *args, **kwargs):
        return render_to_response(
            "agency_landing_page.html",
            dict(agency=self.agency,
                 show_allocation=(
                     'officer_allocation' in settings.INSTALLED_APPS)))


class CallListView(ViewWithAgencies):

    def get(self, request, *args, **kwargs):
        return render_to_response("dashboard.html",
                                  dict(asset_chunk="call_list",
                                       agency=self.agency,
                                       form=build_filter(CallFilterSet)))


class CallVolumeView(ViewWithAgencies):

    def get(self, request, *args, **kwargs):
        return render_to_response("dashboard.html",
                                  dict(asset_chunk="call_volume",
                                       agency=self.agency,
                                       form=build_filter(CallFilterSet)))


class ResponseTimeView(ViewWithAgencies):

    def get(self, request, *args, **kwargs):
        return render_to_response("dashboard.html",
                                  dict(asset_chunk="response_time",
                                       agency=self.agency,
                                       form=build_filter(CallFilterSet)))


class MapView(ViewWithAgencies):

    def get(self, request, *args, **kwargs):
        return render_to_response("dashboard.html",
                                  dict(asset_chunk="call_map",
                                       agency=self.agency,
                                       form=build_filter(CallFilterSet)))


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class CSVIterator:

    def __init__(self, queryset, fields):
        self.queryset = queryset.iterator()
        pseudo_buffer = Echo()
        self.fields = fields
        self.writer = csv.DictWriter(pseudo_buffer, fieldnames=fields)

    def __iter__(self):
        yield self.writer.writerow(dict(zip(self.fields, self.fields)))
        for record in self.queryset:
            serializer = CallExportSerializer(record)
            yield self.writer.writerow(serializer.data)


class CallExportView(ViewWithAgencies):

    def get(self, request, *args, **kwargs):
        qs = Call.objects \
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

        filter_set = CallFilterSet(data=request.GET,
                                   queryset=qs,
                                   strict_mode=StrictMode.fail)

        fields = [
            'call_id',
            'case_id',
            'cancelled',
            'report_only',
            'priority',
            'call_source',
            'nature',
            'nature_group',
            'close_code',

            'time_received',
            'month_received',
            'week_received',
            'dow_received',
            'hour_received',

            'time_routed',
            'time_finished',
            'first_unit_dispatch',
            'first_unit_enroute',
            'first_unit_arrive',
            'first_unit_transport',
            'last_unit_clear',
            'time_closed',
            'officer_response_time',
            'overall_response_time',

            'district',
            'beat',
            'business',
            'street_address',
            'city',
            'zip_code',
            'geox',
            'geoy',

            'primary_unit',
            'first_dispatched',
            'reporting_unit',
        ]

        def grouper(n, iterable):
            it = iter(iterable)
            while True:
                chunk = tuple(itertools.islice(it, n))
                if not chunk:
                    return
                yield chunk

        def data():
            csvfile = StringIO()
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writerow(dict(zip(fields, fields)))
            yield csvfile.getvalue()

            for records in grouper(2000, filter_set.filter().iterator()):
                csvfile = StringIO()
                csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
                serializer = CallExportSerializer(records, many=True)

                for record in serializer.data:
                    csvwriter.writerow(record)

                yield csvfile.getvalue()

        response = StreamingHttpResponse(data(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="calls.csv"'

        return response
