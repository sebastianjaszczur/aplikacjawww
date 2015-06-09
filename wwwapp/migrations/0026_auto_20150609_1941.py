# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0025_userprofile_cover_letter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='participants',
            field=models.ManyToManyField(related_name='workshops', to='wwwapp.UserProfile', blank=True),
            preserve_default=True,
        ),
    ]
