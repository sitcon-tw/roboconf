# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0008_submission_slides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default=b'P', max_length=1, choices=[(b'A', b'Accepted'), (b'R', b'Rejected'), (b'P', b'Pending'), (b'V', b'Reviewing'), (b'E', b'Editing'), (b'Z', b'Ended')]),
            preserve_default=True,
        ),
    ]
