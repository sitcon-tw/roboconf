# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20150208_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='type',
            field=models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Short talk'), (b'L', b'Talk'), (b'N', b'Lightning talk'), (b'K', b'K')]),
            preserve_default=True,
        ),
    ]
