# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0041_auto_20150806_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopcategory',
            name='year',
            field=models.IntegerField(default=2015),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workshoptype',
            name='year',
            field=models.IntegerField(default=2015),
            preserve_default=True,
        ),
    ]
