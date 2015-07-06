# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0031_auto_20150706_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshop',
            name='old_participants',
        ),
    ]
