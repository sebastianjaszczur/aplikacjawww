# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0033_auto_20150707_1900'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workshopparticipant',
            unique_together=set([('workshop', 'participant')]),
        ),
    ]
