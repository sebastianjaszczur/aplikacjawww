# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0002_auto_20150213_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(max_length=100000, blank=True),
            preserve_default=True,
        ),
    ]
