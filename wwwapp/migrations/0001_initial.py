# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wwwapp.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('content', models.TextField(max_length=100000, blank=True)),
                ('on_menubar', models.BooleanField(default=False)),
                ('modified_by', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleContentHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(editable=False)),
                ('content', models.TextField()),
                ('article', models.ForeignKey(to='wwwapp.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(default=None, max_length=10, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='articlecontenthistory',
            unique_together=set([('version', 'article')]),
        ),
    ]
