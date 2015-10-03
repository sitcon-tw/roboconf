# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.crypto
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='abilities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('medical', models.BooleanField(default=False, verbose_name='\u91ab\u7642')),
                ('legal', models.BooleanField(default=False, verbose_name='\u6cd5\u5f8b')),
                ('pr', models.BooleanField(default=False, verbose_name='\u516c\u95dc')),
                ('other', models.CharField(default=b'', help_text=b'other special abilities', max_length=64, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english', models.BooleanField(default=False, verbose_name='\u82f1\u8a9e')),
                ('japanese', models.BooleanField(default=False, verbose_name='\u65e5\u8a9e')),
                ('taiwanese', models.BooleanField(default=False, verbose_name='\u53f0\u8a9e')),
                ('cantonese', models.BooleanField(default=False, verbose_name='\u7cb5\u8a9e')),
                ('other', models.CharField(default=b'', help_text=b'other language abilities', max_length=64, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegisterToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255)),
                ('token', models.CharField(default=django.utils.crypto.get_random_string, max_length=12)),
                ('valid', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(related_name='tokens', to='auth.Group')),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='departure',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='abilities',
            field=models.OneToOneField(related_name='+', null=True, default=None, to='users.abilities', blank=True, help_text=b'other abilities'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='accom',
            field=models.IntegerField(default=0, help_text=b'need for accommodation', choices=[(0, b'Not needed'), (1, b'Either'), (2, b'Needed')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cel_dinner',
            field=models.NullBooleanField(help_text=b'need for celebratory dinner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='certificate',
            field=models.NullBooleanField(help_text=b'need for certificate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='diet',
            field=models.CharField(default=b'', max_length=8, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.IntegerField(blank=True, help_text=b'', null=True, choices=[(1, b'Male'), (2, b'Female'), (9, b'Other')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.OneToOneField(related_name='+', null=True, default=None, to='users.language', blank=True, help_text=b'language abilities'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='personal_id',
            field=models.CharField(default=b'', max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='prev_worker',
            field=models.BooleanField(default=False, help_text=b'if is previously a SITCON worker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='residence',
            field=models.CharField(default=b'', help_text=b'residence', max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='roommate',
            field=models.ForeignKey(related_name='+', default=None, blank=True, to=settings.AUTH_USER_MODEL, help_text=b'requested roommate', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='shirt_size',
            field=models.CharField(default=b'', help_text=b'T-shirt size', max_length=8, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='transportation',
            field=models.CharField(default=b'', help_text=b'way to transport', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='transportation_aid',
            field=models.BooleanField(default=False, help_text=b'if need transportation fee aid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='transportation_fee',
            field=models.CharField(default=b'', help_text=b'transportation fee', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='transportation_hr',
            field=models.BooleanField(default=False, help_text=b'if transportation time >= 1hr'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twenty',
            field=models.BooleanField(default=True, help_text=b'if age >= 20'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default=b'', help_text=b'biography', max_length=320, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='comment',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='display_name',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='grade',
            field=models.CharField(default=b'', help_text=b'department and grade / position', max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default=b'', max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(default=b'', help_text=b'school or company', max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(max_length=16),
            preserve_default=True,
        ),
    ]
