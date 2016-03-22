# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0042_auto_20160322_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('status', models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'Z', 'Zaakceptowany'), (b'O', 'Odrzucony')])),
                ('user_profile', models.ForeignKey(related_name='workshop_profile', to='wwwapp.UserProfile', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
