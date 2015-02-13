# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0005_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='on_menubar',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
