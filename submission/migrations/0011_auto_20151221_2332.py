# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0010_auto_20151202_0944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'permissions': (('view_total_score', 'View total score'),)},
        ),
    ]
