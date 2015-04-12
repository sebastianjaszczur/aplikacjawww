# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0017_auto_20150409_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_page',
            field=models.TextField(default=b'', max_length=100000, blank=True),
            preserve_default=True,
        ),
    ]
