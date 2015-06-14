# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0026_auto_20150609_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='is_qualifying',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
