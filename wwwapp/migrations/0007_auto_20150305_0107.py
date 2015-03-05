# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0006_auto_20150305_0107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshop',
            old_name='title',
            new_name='name',
        ),
    ]
