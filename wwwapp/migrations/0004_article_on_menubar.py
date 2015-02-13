# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0003_auto_20150213_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='on_menubar',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
