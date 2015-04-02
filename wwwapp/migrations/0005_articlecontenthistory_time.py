# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0004_auto_20150402_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecontenthistory',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
