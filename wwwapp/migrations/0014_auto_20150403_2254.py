# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0013_auto_20150403_0030'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='workshop',
            name='type',
            field=models.ForeignKey(default=None, to='wwwapp.WorkshopType', null=True),
            preserve_default=True,
        ),
    ]
