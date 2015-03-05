# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wwwapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0004_auto_20150305_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='name',
            field=wwwapp.models.AlphaNumericField(unique=True, max_length=40),
            preserve_default=True,
        ),
    ]
