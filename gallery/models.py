from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from PIL import Image as pImage
from PIL.ExifTags import TAGS
from gallery import settings
from pathlib import Path
from datetime import datetime
import os


class RotateAccordingToEXIF(object):
    def process(self, image):
        orientation = None
        for orientation in TAGS.keys():
            if TAGS[orientation] == 'Orientation':
                break
        exif = dict(image.getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        return image


class Image(models.Model):

    data = models.ImageField(upload_to='gallery')
    data_thumbnail = ImageSpecField(source='data',
                                    processors=[
                                        RotateAccordingToEXIF(),
                                        ResizeToFit(height=settings.GALLERY_THUMBNAIL_SIZE * settings.GALLERY_HDPI_FACTOR)],
                                    format='JPEG',
                                    options={'quality': settings.GALLERY_RESIZE_QUALITY})
    data_preview = ImageSpecField(source='data',
                                  processors=[
                                        RotateAccordingToEXIF(),
                                        ResizeToFit(width=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR,
                                                    height=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR)],
                                  format='JPEG',
                                  options={'quality': settings.GALLERY_RESIZE_QUALITY})
    date_uploaded = models.DateTimeField(auto_now_add=True)

    # Cached EXIF data
    title = models.CharField(max_length=256)
    exif_date_taken = models.DateTimeField(null=True, blank=True, default=None)
    exif_camera = models.CharField(max_length=128, null=True, blank=True, default=None)
    exif_lens = models.CharField(max_length=128, null=True, blank=True, default=None)
    exif_focal_length = models.CharField(max_length=128, null=True, blank=True, default=None)
    exif_aperture = models.CharField(max_length=128, null=True, blank=True, default=None)
    exif_exposure = models.CharField(max_length=128, null=True, blank=True, default=None)
    exif_iso = models.CharField(max_length=128, null=True, blank=True, default=None)

    @property
    def slug(self):
        return slugify(self.title)

    def update_exif(self):
        exif_data = {}
        self.data.open()
        with pImage.open(self.data) as img:
            if hasattr(img, '_getexif'):
                info = img.getexif()
                if not info:
                    return {}
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif_data[decoded] = value
                # Process some data for easy rendering in template
                exif_data['Camera'] = exif_data.get('Model', '')
                if exif_data.get('Make', '') not in exif_data['Camera']:  # Work around for Canon
                    exif_data['Camera'] = "{0} {1}".format(exif_data['Make'].title(), exif_data['Model'])
                if 'FNumber' in exif_data:
                    exif_data['Aperture'] = str(exif_data['FNumber'][0] / exif_data['FNumber'][1])
                if 'ExposureTime' in exif_data:
                    exif_data['Exposure'] = "{0}/{1}".format(exif_data['ExposureTime'][0],
                                                             exif_data['ExposureTime'][1])
            img.close()

        self.exif_camera = exif_data.get('Camera')
        self.exif_lens = exif_data.get('LensModel')
        self.exif_focal_length = exif_data.get('FocalLengthIn35mmFilm')
        self.exif_aperture = exif_data.get('Aperture')
        self.exif_exposure = exif_data.get('Exposure')
        self.exif_iso = exif_data.get('ISOSpeedRatings')

        self.exif_date_taken = None
        original_exif = exif_data.get('DateTimeOriginal')
        if original_exif:
            try:
                self.exif_date_taken = datetime.strptime(original_exif, "%Y:%m:%d %H:%M:%S")
            except ValueError:  # Fall back to file modification time
                pass

    @property
    def date_taken(self):
        if self.exif_date_taken:
            return self.exif_date_taken
        return self.date_uploaded  # Fall back to upload date if no date taken present

    def update_title(self):
        """ Derive a title from the original filename """
        # remove extension
        filename = Path(self.data.name).with_suffix('').name
        # convert spacing characters to whitespaces
        name = filename.translate(str.maketrans('_', ' '))
        # return with first letter caps
        self.title = name.title()

    def get_absolute_url(self):
        return reverse('gallery:image_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title


@receiver(post_save, sender=Image)
def update_cached_exif(sender, instance, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    if not instance.title:
        instance.update_title()
    instance.update_exif()

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty


class Album(models.Model):
    title = models.CharField(max_length=250)
    images = models.ManyToManyField(Image, blank=True, related_name='image_albums')
    highlight = models.OneToOneField(Image,
                                     related_name='album_highlight',
                                     null=True, blank=True,
                                     on_delete=models.SET_NULL,
                                     )
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['order', '-pk']

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def display_highlight(self):
        # if there is no highlight but there are images in the album, use the first
        if not self.highlight and self.images.count():
            image = self.images.earliest('id')
        else:
            image = self.highlight
        if image:
            image.title = self.title  # use the album title instead of the highlight title
        return image

    def get_absolute_url(self):
        return reverse('gallery:album_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title
