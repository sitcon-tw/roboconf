# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shortname', models.CharField(help_text=b'Short room name', max_length=5)),
                ('fullname', models.CharField(help_text=b'Full room name', max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='submission',
            name='room',
            field=models.ForeignKey(blank=True, to='submission.Room', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submission',
            name='time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
