# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0036_userprofile_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pesel', models.CharField(default=b'', max_length=20, blank=True)),
                ('address', models.TextField(default=b'', max_length=1000, blank=True)),
                ('start_date', models.CharField(default=b'no_idea', max_length=100, choices=[(b'no_idea', 'Nie ogarniam'), ('17', '17 sierpien'), ('18', '18 sierpien'), ('19', '19 sierpien'), ('20', '20 sierpien'), ('21', '21 sierpien'), ('22', '22 sierpien'), ('23', '23 sierpien'), ('24', '24 sierpien'), ('25', '25 sierpien'), ('26', '26 sierpien'), ('27', '27 sierpien'), ('28', '28 sierpien')])),
                ('end_date', models.CharField(default=b'no_idea', max_length=100, choices=[(b'no_idea', 'Nie ogarniam'), ('17', '17 sierpien'), ('18', '18 sierpien'), ('19', '19 sierpien'), ('20', '20 sierpien'), ('21', '21 sierpien'), ('22', '22 sierpien'), ('23', '23 sierpien'), ('24', '24 sierpien'), ('25', '25 sierpien'), ('26', '26 sierpien'), ('27', '27 sierpien'), ('28', '28 sierpien')])),
                ('meeting_point', models.CharField(default=b'no_idea', max_length=100, choices=[(b'no_idea', 'Nie ogarniam'), (b'wierchomla', 'Wierchomla Wielka'), (b'warsaw', 'Warszawa'), (b'cracow', 'Krak\xf3w')])),
                ('tshirt_size', models.CharField(default=b'no_idea', max_length=100, choices=[(b'no_idea', 'Nie ogarniam'), (b'XS', 'XS'), (b'S', 'S'), (b'M', 'M'), (b'L', 'L'), (b'XL', 'XL'), (b'XXL', 'XXL')])),
                ('comments', models.CharField(default=b'', max_length=1000, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='userinfo',
            field=models.OneToOneField(default=None, to='wwwapp.UserInfo', null=True),
            preserve_default=False,
        ),
    ]
