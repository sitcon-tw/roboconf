# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(related_name='folders', blank=True, to='docs.Folder', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='starring',
            field=models.ManyToManyField(related_name='starred_folders', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
