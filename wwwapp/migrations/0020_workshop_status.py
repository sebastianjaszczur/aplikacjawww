# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0019_remove_userprofile_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='status',
            field=models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'Z', 'Zaakceptowane'), (b'O', 'Odrzucone')]),
            preserve_default=True,
        ),
    ]
