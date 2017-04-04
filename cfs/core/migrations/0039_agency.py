# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    """Create an initial agency."""
    Agency = apps.get_model("core", "Agency")
    SiteConfiguration = apps.get_model("core", "SiteConfiguration")
    agency = Agency()
    try:
        config = SiteConfiguration.objects.get()
        if config.department_abbr and config.department_name:
            agency.code = config.department_abbr
            agency.descr = config.department_name
        else:
            agency.code = "CPD"
            agency.descr = "City Police Department"
    except SiteConfiguration.DoesNotExist:
        agency.code = "CPD"
        agency.descr = "City Police Department"
    agency.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_callunit_is_patrol_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('code', models.CharField(unique=True,
                                          verbose_name='Unique code', max_length=64)),
                ('descr', models.CharField(verbose_name='Description', max_length=255)),
                ('agency_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'agency',
            },
        ),
        migrations.RunPython(forwards_func, migrations.RunPython.noop)
    ]
