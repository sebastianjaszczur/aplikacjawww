# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0035_workshopparticipant_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'Z', 'Zaakceptowany'), (b'O', 'Odrzucony')]),
            preserve_default=True,
        ),
    ]
