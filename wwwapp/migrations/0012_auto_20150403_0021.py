# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0011_auto_20150402_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='lecturer',
            field=models.ManyToManyField(to='wwwapp.UserProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workshop',
            name='title',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workshop',
            name='name',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
    ]
