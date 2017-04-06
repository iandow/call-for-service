# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_callunit_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='projection',
            field=models.CharField(max_length=1023, blank=True, null=True,
                                   help_text="The projection definition for this agency's geo coordinates, as seen on https://github.com/proj4js/proj4js. If you do not know what this is, you likely do not need it."),
        ),
    ]
