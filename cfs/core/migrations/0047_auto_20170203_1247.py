# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_callunit_agency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('descr', models.TextField(unique=True, verbose_name='Description')),
                ('department_id', models.AutoField(
                    primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='use_department',
            field=models.BooleanField(
                default=False, verbose_name='Use department?'),
        ),
        migrations.AddField(
            model_name='call',
            name='department',
            field=models.ForeignKey(
                to='core.Department', null=True, blank=True),
        ),
    ]
