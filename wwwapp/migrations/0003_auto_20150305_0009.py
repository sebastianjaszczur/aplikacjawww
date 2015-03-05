# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0002_articlecontenthistory_modified_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='how_do_you_know_about',
            field=models.CharField(default=b'', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='interests',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='matura_exam_year',
            field=models.PositiveSmallIntegerField(default=None, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='school',
            field=models.CharField(default=b'', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=None, max_length=10, null=True, choices=[(b'M', 'M\u0119\u017cczyzna'), (b'F', 'Kobieta')]),
            preserve_default=True,
        ),
    ]
