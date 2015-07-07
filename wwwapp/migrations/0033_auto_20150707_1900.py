# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0032_remove_workshop_old_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='qualification_threshold',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workshopparticipant',
            name='qualification_result',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True),
            preserve_default=True,
        ),
    ]
