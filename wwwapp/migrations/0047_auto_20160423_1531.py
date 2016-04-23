# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0046_auto_20160324_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userinfo',
            field=annoying.fields.AutoOneToOneField(to='wwwapp.UserInfo'),
            preserve_default=True,
        ),
    ]
