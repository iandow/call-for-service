# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_agency'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='agency',
            field=models.ForeignKey(to='core.Agency', null=True, blank=True),
        ),
    ]
