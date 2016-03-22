# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0044_auto_20160322_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='status',
        ),
    ]
