# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0006_auto_20150212_0009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='room',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='time',
        ),
        migrations.AlterField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(related_name='submissions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
