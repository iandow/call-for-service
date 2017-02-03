from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.html import mark_safe, format_html


def navbar(context, *args, **kwargs):
    if context['agency']:
        return mark_safe("<li><a href='{}'>Officer Allocation</a></li>".format(
            reverse('officer_allocation', kwargs={'agency_code': context['agency'].code})))
    else:
        return ''
