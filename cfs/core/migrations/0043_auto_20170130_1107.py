# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20170124_1517'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sector',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='sector',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='beat',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='call',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='district',
            name='sector',
        ),
        migrations.DeleteModel(
            name='Sector',
        ),
    ]
