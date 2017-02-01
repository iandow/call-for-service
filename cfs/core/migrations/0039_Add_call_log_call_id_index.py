# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_callunit_is_patrol_unit'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE INDEX call_log_call_id_ndx ON call_log (call_id)
            """,
            """
            DROP INDEX call_log_call_id_ndx;
            """
        ),
    ]
