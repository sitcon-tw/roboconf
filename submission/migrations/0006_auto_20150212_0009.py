# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0005_auto_20150212_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='type',
            field=models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Short talk'), (b'L', b'Talk'), (b'N', b'Lightning talk'), (b'K', b'Keynote')]),
            preserve_default=True,
        ),
    ]
