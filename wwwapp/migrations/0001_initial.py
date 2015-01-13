# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wwwapp.models
import sanitizer.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', wwwapp.models.AlphaNumericField(max_length=40)),
                ('content', sanitizer.models.SanitizedTextField(max_length=100000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
