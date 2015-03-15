# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0007_auto_20150315_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='slides',
            field=models.TextField(default='', help_text=b'links to slides', blank=True),
            preserve_default=False,
        ),
    ]
