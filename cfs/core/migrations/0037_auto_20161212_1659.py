# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20161212_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_end',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_start',
            field=models.BooleanField(default=False),
        ),
    ]
