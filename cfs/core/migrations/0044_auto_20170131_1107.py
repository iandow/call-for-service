# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20170130_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='geo_center',
            field=geoposition.fields.GeopositionField(
                blank=True, verbose_name='Center', max_length=42),
        ),
        migrations.AddField(
            model_name='agency',
            name='geo_default_zoom',
            field=models.PositiveIntegerField(
                default=11, verbose_name='Default zoom level'),
        ),
        migrations.AddField(
            model_name='agency',
            name='geo_ne_bound',
            field=geoposition.fields.GeopositionField(
                blank=True, verbose_name='Northeast bound', max_length=42),
        ),
        migrations.AddField(
            model_name='agency',
            name='geo_sw_bound',
            field=geoposition.fields.GeopositionField(
                blank=True, verbose_name='Southwest bound', max_length=42),
        ),
        migrations.AddField(
            model_name='agency',
            name='geojson_url',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
    ]
