# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submission.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('audience', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('cool', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('expression', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('difficulty', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=40)),
                ('type', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Short talk'), (b'L', b'Talk'), (b'N', b'Lightning talk')])),
                ('avatar', models.CharField(help_text=b'link to custom avatar image', max_length=1000, blank=True)),
                ('abstract', models.TextField(max_length=500)),
                ('details', models.TextField(blank=True)),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'A', b'Accepted'), (b'R', b'Rejected'), (b'P', b'Pending'), (b'V', b'Reviewing')])),
                ('comment', models.TextField(help_text=b'Review comment', blank=True)),
                ('user', models.ForeignKey(related_name='submissions', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('review', 'Review submissions'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubmissionFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=submission.models.file_path)),
                ('submission', models.ForeignKey(related_name='files', to='submission.Submission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='score',
            name='submission',
            field=models.ForeignKey(related_name='scores', to='submission.Submission'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='score',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('submission', 'user')]),
        ),
    ]
