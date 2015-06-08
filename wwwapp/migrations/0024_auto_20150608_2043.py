# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0023_workshop_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='qualification_problems',
            field=models.FileField(null=True, upload_to=b'qualification', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workshop',
            name='type',
            field=models.ForeignKey(default=None, blank=True, to='wwwapp.WorkshopType', null=True),
            preserve_default=True,
        ),
    ]
