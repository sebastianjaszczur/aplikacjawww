# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0040_auto_20150726_0036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'permissions': (('see_user_info', 'Can see user info'),)},
        ),
    ]
