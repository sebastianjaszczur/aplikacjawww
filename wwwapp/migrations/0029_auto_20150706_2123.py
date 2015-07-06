# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0028_auto_20150706_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='old_participants',
            field=models.ManyToManyField(related_name='old_workshops', to='wwwapp.UserProfile', blank=True),
            preserve_default=True,
        ),
    ]
