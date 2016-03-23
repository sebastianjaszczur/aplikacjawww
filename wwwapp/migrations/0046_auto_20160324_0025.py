# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0045_remove_userprofile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopcategory',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workshopcategory',
            name='year',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workshoptype',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workshoptype',
            name='year',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='workshopcategory',
            unique_together=set([('year', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='workshoptype',
            unique_together=set([('year', 'name')]),
        ),
    ]
