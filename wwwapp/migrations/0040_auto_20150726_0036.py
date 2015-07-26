# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def combine_names(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    UserProfile = apps.get_model("wwwapp", "UserProfile")
    UserInfo = apps.get_model("wwwapp", "UserInfo")
    for user_profile in UserProfile.objects.all():
        if user_profile.userinfo is None:
            userinfo = UserInfo.objects.create()
            userinfo.save()
            user_profile.userinfo = userinfo
            user_profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0039_auto_20150726_0034'),
    ]

    operations = [
        migrations.RunPython(combine_names),
        migrations.AlterField(
            model_name='userprofile',
            name='userinfo',
            field=models.OneToOneField(to='wwwapp.UserInfo'),
            preserve_default=True,
        ),
    ]
