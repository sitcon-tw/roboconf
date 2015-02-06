# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20150206_0042'),
        ('submission', '0002_auto_20150205_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='room',
            field=models.ForeignKey(blank=True, to='schedule.Room', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
