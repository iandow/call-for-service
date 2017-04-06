# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_agency_projection'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='coords_flipped',
            field=models.BooleanField(
                default=False, help_text='Are your coordinates flipped in the database?'),
        ),
    ]
