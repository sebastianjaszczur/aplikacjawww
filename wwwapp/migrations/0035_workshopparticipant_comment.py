# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0034_auto_20150707_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopparticipant',
            name='comment',
            field=models.CharField(default=None, max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
