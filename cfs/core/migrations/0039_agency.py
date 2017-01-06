# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


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
    ]
