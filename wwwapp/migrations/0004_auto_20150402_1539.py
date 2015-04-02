# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0003_auto_20150305_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='name',
            field=models.SlugField(help_text=b'Nazwa w URLach.', unique=True),
            preserve_default=True,
        ),
    ]
