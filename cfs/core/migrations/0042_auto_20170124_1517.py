# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.db import migrations, models


def set_agency_defaults(apps, schema_editor):
    Agency = apps.get_model('core', 'Agency')
    District = apps.get_model('core', 'District')
    Sector = apps.get_model('core', 'Sector')

    agency = Agency.objects.first()
    District.objects.update(agency=agency)
    Sector.objects.update(agency=agency)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20170111_1432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['descr']},
        ),
        migrations.AlterModelOptions(
            name='sector',
            options={'ordering': ['descr']},
        ),
        migrations.AddField(
            model_name='district',
            name='agency',
            field=models.ForeignKey(to='core.Agency', null=True),
        ),
        migrations.AddField(
            model_name='sector',
            name='agency',
            field=models.ForeignKey(to='core.Agency', null=True),
        ),
        migrations.RunPython(set_agency_defaults, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='district',
            name='agency',
            field=models.ForeignKey(to='core.Agency'),
        ),
        migrations.AlterField(
            model_name='sector',
            name='agency',
            field=models.ForeignKey(to='core.Agency'),
        ),
        migrations.AlterField(
            model_name='district',
            name='descr',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='sector',
            name='descr',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set([('agency', 'descr')]),
        ),
        migrations.AlterUniqueTogether(
            name='sector',
            unique_together=set([('agency', 'descr')]),
        ),
    ]
