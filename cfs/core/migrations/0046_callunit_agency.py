# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_callunit_agency(apps, schema_editor):
    Agency = apps.get_model('core', 'Agency')
    CallUnit = apps.get_model('core', 'CallUnit')
    agency = Agency.objects.first()

    CallUnit.objects.update(agency=agency)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='callunit',
            name='agency',
            field=models.ForeignKey(to='core.Agency', blank=True, null=True),
        ),
        migrations.RunPython(set_callunit_agency, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='callunit',
            name='agency',
            field=models.ForeignKey(to='core.Agency'),
        ),
    ]
