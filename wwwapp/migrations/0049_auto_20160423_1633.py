# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0048_auto_20160423_1633'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='userinfo',
            new_name='user_info',
        ),
    ]
