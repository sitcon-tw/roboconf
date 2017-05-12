# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-12 09:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.crypto
import users.models


class Migration(migrations.Migration):

    replaces = [(b'users', '0001_initial'), (b'users', '0002_auto_20151003_0935'), (b'users', '0003_auto_20151227_0016'), (b'users', '0004_auto_20160417_0435'), (b'users', '0005_auto_20160428_2230'), (b'users', '0006_auto_20160501_2315'), (b'users', '0007_auto_20170508_0251')]

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'GroupCategory',
            fields=[
                (b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
                (b'name', models.CharField(max_length=30)),
                (b'is_visible', models.BooleanField(default=True)),
                (b'groups', models.ManyToManyField(related_name=b'categories', to=b'auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name=b'UserProfile',
            fields=[
                (b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
                (b'display_name', models.CharField(default=b'Not set', max_length=16)),
                (b'title', models.CharField(default=b'Not set', max_length=16)),
                (b'school', models.CharField(blank=True, help_text=b'school or company', max_length=32)),
                (b'bio', models.TextField(help_text=b'biography', max_length=300)),
                (b'grade', models.CharField(blank=True, help_text=b'department and grade / position', max_length=32)),
                (b'phone', models.CharField(blank=True, max_length=16)),
                (b'photo', models.FileField(blank=True, upload_to=users.models.photo_path)),
                (b'comment', models.TextField(blank=True)),
                (b'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name=b'profile', to=settings.AUTH_USER_MODEL)),
                (b'abilities', models.OneToOneField(blank=True, default=None, help_text=b'other abilities', null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'+', to=b'users.abilities')),
                (b'accom', models.IntegerField(choices=[(0, b'Not needed'), (1, b'Either'), (2, b'Needed')], default=0, help_text=b'need for accommodation')),
                (b'cel_dinner', models.NullBooleanField(help_text=b'need for celebratory dinner')),
                (b'certificate', models.NullBooleanField(help_text=b'need for certificate')),
                (b'diet', models.CharField(blank=True, default=b'', max_length=8)),
                (b'gender', models.IntegerField(blank=True, choices=[(1, b'Male'), (2, b'Female'), (9, b'Other')], help_text=b'', null=True)),
            ],
        ),
        migrations.CreateModel(
            name=b'language',
            fields=[
                (b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
                (b'english', models.BooleanField(default=False, verbose_name=b'\xe8\x8b\xb1\xe8\xaa\x9e')),
                (b'japanese', models.BooleanField(default=False, verbose_name=b'\xe6\x97\xa5\xe8\xaa\x9e')),
                (b'taiwanese', models.BooleanField(default=False, verbose_name=b'\xe5\x8f\xb0\xe8\xaa\x9e')),
                (b'cantonese', models.BooleanField(default=False, verbose_name=b'\xe7\xb2\xb5\xe8\xaa\x9e')),
                (b'other', models.CharField(blank=True, default='', help_text='other language abilities', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name=b'RegisterToken',
            fields=[
                (b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
                (b'title', models.CharField(blank=True, default=b'', max_length=255)),
                (b'token', models.CharField(default=django.utils.crypto.get_random_string, max_length=12)),
                (b'valid', models.BooleanField(default=True)),
                (b'groups', models.ManyToManyField(related_name=b'tokens', to=b'auth.Group')),
                (b'user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('display_name', models.CharField(blank=True, default=b'', max_length=255)),
                ('email', models.CharField(blank=True, default=b'', max_length=255)),
                ('username', models.CharField(blank=True, default=b'', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'language',
            field=models.OneToOneField(blank=True, default=None, help_text=b'language abilities', null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'+', to=b'users.language'),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'personal_id',
            field=models.CharField(blank=True, default=b'', max_length=16),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'prev_worker',
            field=models.BooleanField(default=False, help_text=b'if is previously a SITCON worker'),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'residence',
            field=models.CharField(blank=True, default=b'', help_text=b'residence', max_length=16),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'roommate',
            field=models.ForeignKey(blank=True, default=None, help_text=b'requested roommate', null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'shirt_size',
            field=models.CharField(blank=True, default=b'', help_text=b'T-shirt size', max_length=8),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'transportation',
            field=models.CharField(blank=True, default=b'', help_text=b'way to transport', max_length=64),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'transportation_aid',
            field=models.BooleanField(default=False, help_text=b'if need transportation fee aid'),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'transportation_fee',
            field=models.CharField(blank=True, default=b'', help_text=b'transportation fee', max_length=64),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'transportation_hr',
            field=models.BooleanField(default=False, help_text=b'if transportation time >= 1hr'),
        ),
        migrations.AddField(
            model_name=b'userprofile',
            name=b'twenty',
            field=models.BooleanField(default=True, help_text=b'if age >= 20'),
        ),
        migrations.AlterField(
            model_name=b'userprofile',
            name=b'bio',
            field=models.TextField(blank=True, default=b'', help_text=b'biography', max_length=320),
        ),
        migrations.AlterField(
            model_name=b'userprofile',
            name=b'comment',
            field=models.TextField(blank=True, default=b''),
        ),
        migrations.AlterField(
            model_name=b'userprofile',
            name=b'display_name',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name=b'userprofile',
            name=b'grade',
            field=models.CharField(blank=True, default=b'', help_text=b'department and grade / position', max_length=32),
        ),
        migrations.AlterField(
            model_name=b'userprofile',
            name=b'phone',
            field=models.CharField(blank=True, default=b'', max_length=16),
        ),
        migrations.AlterField(
            model_name=b'userprofile',
            name=b'school',
            field=models.CharField(blank=True, default=b'', help_text=b'school or company', max_length=32),
        ),
        migrations.AlterField(
            model_name=b'userprofile',
            name=b'title',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterModelOptions(
            name=b'userprofile',
            options={b'permissions': ((b'view_profile_detail', b'View profile detail'),)},
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='personal_id',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lead_team',
            field=models.ForeignKey(blank=True, default=None, help_text='leading team', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='abilities',
            field=models.OneToOneField(blank=True, default=None, help_text='other abilities', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.abilities'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='accom',
            field=models.IntegerField(choices=[(0, 'Not needed'), (1, 'Either'), (2, 'Needed')], default=0, help_text='need for accommodation'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default='', help_text='biography', max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cel_dinner',
            field=models.NullBooleanField(help_text='need for celebratory dinner'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='certificate',
            field=models.NullBooleanField(help_text='need for certificate'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='diet',
            field=models.CharField(blank=True, default='', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='display_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (9, 'Other')], null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='grade',
            field=models.CharField(blank=True, default='', help_text='department and grade / position', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.OneToOneField(blank=True, default=None, help_text='language abilities', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.language'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='prev_worker',
            field=models.NullBooleanField(default=False, help_text='if is previously a COSCUP worker'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='residence',
            field=models.CharField(blank=True, default='', help_text='residence', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='roommate',
            field=models.CharField(blank=True, default='', help_text='requested roommate', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(blank=True, default='', help_text='school or company', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='shirt_size',
            field=models.CharField(blank=True, default='', help_text='T-shirt size', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='transportation',
            field=models.CharField(blank=True, default='', help_text='transportation method', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='transportation_aid',
            field=models.NullBooleanField(default=False, help_text='if need transportation fee aid'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='transportation_fee',
            field=models.CharField(blank=True, default='', help_text='transportation fee', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='transportation_hr',
            field=models.NullBooleanField(default=False, help_text='if transportation time >= 1hr'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twenty',
            field=models.NullBooleanField(default=True, help_text='if age >= 20'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birthday',
            field=models.CharField(blank=True, default='', help_text='birthday, for insurance', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ice_contact',
            field=models.CharField(blank=True, default='', help_text='Emergency contact info', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ice_phone',
            field=models.CharField(blank=True, default='', help_text='emergency contact number', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='on_site',
            field=models.NullBooleanField(default=True, help_text='if is onsite volunteer'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='personal_id',
            field=models.CharField(blank=True, default='', help_text='id number, for insurance', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='accom',
            field=models.IntegerField(choices=[(0, 'Not needed'), (1, 'Either'), (2, 'Needed')], default=2, help_text='need for accommodation'),
        ),
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical', models.BooleanField(default=False, verbose_name=b'\xe9\x86\xab\xe7\x99\x82')),
                ('legal', models.BooleanField(default=False, verbose_name=b'\xe6\xb3\x95\xe5\xbe\x8b')),
                ('pr', models.BooleanField(default=False, verbose_name=b'\xe5\x85\xac\xe9\x97\x9c')),
                ('other', models.CharField(blank=True, default=b'', help_text=b'other special abilities', max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='abilities',
            field=models.OneToOneField(blank=True, default=None, help_text=b'other abilities', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.Ability'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default=b'', help_text=b'biography', max_length=512),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='comment',
            field=models.TextField(blank=True, default=b'', max_length=512),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='display_name',
            field=models.CharField(blank=True, default=b'', max_length=32),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, b'Male'), (2, b'Female'), (9, b'Other')], help_text=b'', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='grade',
            field=models.CharField(blank=True, default=b'', help_text=b'department and grade / position', max_length=32),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.OneToOneField(blank=True, default=None, help_text=b'language abilities', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.Language'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default=b'', max_length=16),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(blank=True, default=b'', help_text=b'school or company', max_length=32),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(blank=True, default=b'', max_length=32),
        ),
    ]
