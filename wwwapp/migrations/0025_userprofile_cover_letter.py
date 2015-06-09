# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0024_auto_20150608_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cover_letter',
            field=models.TextField(default=b'', max_length=100000, blank=True),
            preserve_default=True,
        ),
    ]
