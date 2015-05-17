# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0020_workshop_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='page_content',
            field=models.TextField(default='', max_length=100000, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workshop',
            name='page_content_is_public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
