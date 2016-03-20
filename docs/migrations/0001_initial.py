# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlobText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('format', models.CharField(default=b' ', max_length=1, choices=[(b' ', b'Plain text'), (b'M', b'Markdown text'), (b'<', b'HTML document'), (b'B', b'Binary content')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_archived', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
                'permissions': (('archive', 'Archive files and folders'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(related_name='folders', to='docs.Folder', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permalink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('valid_since', models.DateTimeField(null=True)),
                ('file', models.ForeignKey(related_name='permalinks', to='docs.File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, choices=[(b'1', b'View document'), (b'2', b'Comment on document'), (b'3', b'Edit document')])),
                ('effect', models.CharField(max_length=1, choices=[(b'A', b'Allow'), (b'D', b'Deny')])),
                ('scope', models.CharField(max_length=1, choices=[(b'0', b'Public'), (b'1', b'Staff'), (b'2', b'Administrators'), (b'G', b'Specify group'), (b'U', b'Specify user')])),
                ('target', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'.', max_length=1, choices=[(b'.', b'Local revision'), (b'+', b'External linked file')])),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('comment', models.TextField()),
                ('base_revision', models.OneToOneField(related_name='derived_revision', null=True, to='docs.Revision')),
                ('file', models.ForeignKey(related_name='revisions', to='docs.File', null=True)),
                ('text', models.ForeignKey(related_name='revisions', to='docs.BlobText')),
                ('user', models.ForeignKey(related_name='doc_revisions', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='permalink',
            name='revision',
            field=models.ForeignKey(related_name='permalinks', to='docs.Revision', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='permissions',
            field=models.ManyToManyField(related_name='folderperm+', to='docs.Permission'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='starring',
            field=models.ManyToManyField(related_name='starred_folders', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='current_revision',
            field=models.ForeignKey(related_name='currev+', on_delete=django.db.models.deletion.PROTECT, to='docs.Revision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='parent',
            field=models.ForeignKey(related_name='files', to='docs.Folder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='permissions',
            field=models.ManyToManyField(related_name='fileperm+', to='docs.Permission'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='starring',
            field=models.ManyToManyField(related_name='starred_files', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
