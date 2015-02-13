# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0007_auto_20150213_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='just_registered',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
