# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_call_agency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agency',
            options={'verbose_name_plural': 'agencies'},
        ),
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='department_abbr',
        ),
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='department_name',
        ),
        migrations.AlterField(
            model_name='agency',
            name='code',
            field=models.CharField(validators=[django.core.validators.RegexValidator(
                regex='^[A-Za-z0-9]+$')], max_length=64, verbose_name='Unique code', unique=True),
        ),
    ]
