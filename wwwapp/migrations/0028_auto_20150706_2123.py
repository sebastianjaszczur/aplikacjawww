# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0027_workshop_is_qualifying'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshop',
            old_name='participants',
            new_name='old_participants',
        ),
    ]
