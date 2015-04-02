# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0006_auto_20150402_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': (('can_put_on_menubar', 'Can put on menubar'),)},
        ),
    ]
