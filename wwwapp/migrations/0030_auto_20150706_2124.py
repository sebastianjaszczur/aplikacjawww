# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0029_auto_20150706_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('participant', models.ForeignKey(to='wwwapp.UserProfile')),
                ('workshop', models.ForeignKey(to='wwwapp.Workshop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='workshop',
            name='participants',
            field=models.ManyToManyField(related_name='workshops', through='wwwapp.WorkshopParticipant', to='wwwapp.UserProfile', blank=True),
            preserve_default=True,
        ),
    ]
