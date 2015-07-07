# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def copy_participants(apps, schema_editor):
    Workshop = apps.get_model("wwwapp", "Workshop")
    WorkshopParticipant = apps.get_model("wwwapp", "WorkshopParticipant")
    for workshop in Workshop.objects.all():
        for participant in workshop.old_participants.all():
            WorkshopParticipant(workshop=workshop, participant=participant).save()

class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0030_auto_20150706_2124'),
    ]

    operations = [
        migrations.RunPython(copy_participants)
    ]
