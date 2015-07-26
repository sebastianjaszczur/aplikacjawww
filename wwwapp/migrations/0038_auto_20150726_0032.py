# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0037_auto_20150726_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userinfo',
            field=models.OneToOneField(null=True, to='wwwapp.UserInfo'),
            preserve_default=True,
        ),
    ]
