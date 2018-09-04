# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_list', '0003_auto_20170216_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_hidden',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=20480),
            preserve_default=True,
        ),
    ]
