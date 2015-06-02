# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0022_workshop_qualification_problems'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='participants',
            field=models.ManyToManyField(related_name='+', to='wwwapp.UserProfile', blank=True),
            preserve_default=True,
        ),
    ]
