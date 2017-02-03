# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_callunit_agency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='callunit',
            options={'ordering': ['descr']},
        ),
        migrations.AlterField(
            model_name='callunit',
            name='descr',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterUniqueTogether(
            name='callunit',
            unique_together=set([('agency', 'descr')]),
        ),
    ]
