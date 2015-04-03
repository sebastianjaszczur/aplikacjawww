# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0004_auto_20150305_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshop',
            old_name='proposition_descrption',
            new_name='proposition_description',
        ),
        migrations.AlterField(
            model_name='workshop',
            name='title',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
