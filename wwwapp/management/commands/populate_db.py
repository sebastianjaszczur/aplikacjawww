from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = ''
    help = 'Populate the database with data for development'

    def handle(self, *args, **options):
        print("ASDF")