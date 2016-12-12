# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20161209_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='callsource',
            name='is_self_initiated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nature',
            name='is_directed_patrol',
            field=models.BooleanField(default=False),
        ),
    ]
