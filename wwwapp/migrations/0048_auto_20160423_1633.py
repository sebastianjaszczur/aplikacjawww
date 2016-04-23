# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0047_auto_20160423_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userinfo',
            field=models.OneToOneField(to='wwwapp.UserInfo'),
            preserve_default=True,
        ),
    ]
