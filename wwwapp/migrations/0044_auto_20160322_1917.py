# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def move_status(apps, schema_editor):
    UserProfile = apps.get_model('wwwapp', 'UserProfile')
    WorkshopUserProfile = apps.get_model('wwwapp', 'WorkshopUserProfile')
    db_alias = schema_editor.connection.alias

    profiles = list(UserProfile.objects.using(db_alias).all())

    new = []
    for profile in profiles:
        wprofile = WorkshopUserProfile(year=2015, status=profile.status, user_profile=profile)
        wprofile.save(using=db_alias)

class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0043_workshopuserprofile'),
    ]

    operations = [
        migrations.RunPython(move_status)
    ]
