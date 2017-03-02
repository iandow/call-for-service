# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='callunit',
            name='department',
            field=models.ForeignKey(null=True, blank=True, to='core.Department'),
        ),
    ]
