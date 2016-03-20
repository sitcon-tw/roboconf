# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('is_visible', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(related_name='categories', to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(default=b'Not set', max_length=16)),
                ('title', models.CharField(default=b'Not set', max_length=16)),
                ('school', models.CharField(help_text=b'school or company', max_length=32, blank=True)),
                ('bio', models.TextField(help_text=b'biography', max_length=300)),
                ('grade', models.CharField(help_text=b'department and grade / position', max_length=32, blank=True)),
                ('phone', models.CharField(max_length=16, blank=True)),
                ('photo', models.FileField(upload_to=users.models.photo_path, blank=True)),
                ('departure', models.CharField(help_text=b'departure', max_length=10, blank=True)),
                ('comment', models.TextField(blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
