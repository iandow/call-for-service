# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20170111_1432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['descr']},
        ),
        migrations.AlterModelOptions(
            name='sector',
            options={'ordering': ['descr']},
        ),
        migrations.AddField(
            model_name='district',
            name='agency',
            field=models.ForeignKey(to='core.Agency', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sector',
            name='agency',
            field=models.ForeignKey(to='core.Agency', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='district',
            name='descr',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='sector',
            name='descr',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set([('agency', 'descr')]),
        ),
        migrations.AlterUniqueTogether(
            name='sector',
            unique_together=set([('agency', 'descr')]),
        ),
    ]
