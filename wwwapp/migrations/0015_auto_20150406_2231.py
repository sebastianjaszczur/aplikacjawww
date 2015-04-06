# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0014_auto_20150403_2254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workshop',
            options={'permissions': (('can_see_all', 'Can see all'),)},
        ),
    ]
