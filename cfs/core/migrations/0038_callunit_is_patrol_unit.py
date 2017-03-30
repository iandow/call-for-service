# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20161212_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='callunit',
            name='is_patrol_unit',
            field=models.BooleanField(default=True),
        ),
    ]
