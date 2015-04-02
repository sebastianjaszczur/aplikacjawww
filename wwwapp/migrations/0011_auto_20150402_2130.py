# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0010_auto_20150402_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'M', 'M\u0119\u017cczyzna'), (b'F', 'Kobieta')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='matura_exam_year',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
