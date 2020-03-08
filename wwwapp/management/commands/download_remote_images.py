import hashlib
import mimetypes
import os.path
import re
import requests
from urllib.parse import urljoin

from django.core.management.base import BaseCommand

import wwwapp.settings as settings
from wwwapp.models import Workshop, Article


class Command(BaseCommand):
    help = 'Download all images referenced in <img> tags in old descriptions and upgrade to storing them on our server'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--dryrun', action='store_true', help='Do not write anything to the database')
        group.add_argument('--force', action='store_true', help='Actually upgrade the database')

    def handle(self, *args, **options):
        assert options['dryrun'] or options['force']
        for article in Article.objects.all():
            print("Upgrading Article {}".format(article.name))
            article.content = self.update_description(article.content, "images/articles/{}/".format(article.name), options['dryrun'])
            if not options['dryrun']:
                article.save()
        for workshop in Workshop.objects.all():
            print("Upgrading Workshop {} {}".format(workshop.type.year, workshop.name))
            workshop.page_content = self.update_description(workshop.page_content, "images/workshops/{}/".format(workshop.name), options['dryrun'])
            if not options['dryrun']:
                workshop.save()
        if options['dryrun']:
            print("Dry run finished succesfully")
        else:
            print("Database upgraded succesfully")

    @staticmethod
    def update_description(text, path, dryrun):
        def update_img(m):
            url = m.group(1)
            if not url.startswith("http://") and not url.startswith("https://"):
                return m.group(0)
            print("Downloading {}".format(url))
            r = requests.get(url)
            if r.status_code != 200:
                print("WARNING: {} returned {}".format(url, r.status_code))
                return m.group(0)
            else:
                if 'Content-Type' not in r.headers:
                    raise Exception("Server didn't provide a Content-Type for the file")
                ext = mimetypes.guess_extension(r.headers['Content-Type'].split(";")[0])
                if ext is None:
                    raise Exception("Unable to determine file extension for " + r.headers['Content-Type'])
                fname = hashlib.sha256(r.content).hexdigest() + ext
                fpath = os.path.join(settings.MEDIA_ROOT, path, fname)
                print("Saving to {}".format(fpath))
                if not dryrun:
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, path), exist_ok=True)
                    with open(fpath, 'wb+') as destination:
                        destination.write(r.content)
                newurl = urljoin(urljoin(settings.MEDIA_URL, path), fname)
                print("New URL is {}".format(newurl))
                return m.group(0).replace(url, newurl)

        return re.sub(r'<img.*?src="(.*?)".*?>', update_img, text)
