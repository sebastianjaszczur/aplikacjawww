# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0009_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='name',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
    ]
