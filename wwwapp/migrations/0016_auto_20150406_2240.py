# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0015_auto_20150406_2231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workshop',
            options={'permissions': (('see_all_workshops', 'Can see all workshops'),)},
        ),
    ]
