# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('task_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status_changed_by',
            field=models.ForeignKey(related_name='changed_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
