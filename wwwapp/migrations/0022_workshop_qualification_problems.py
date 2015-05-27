# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0021_auto_20150517_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='qualification_problems',
            field=models.FileField(null=True, upload_to=b'qualification'),
            preserve_default=True,
        ),
    ]
