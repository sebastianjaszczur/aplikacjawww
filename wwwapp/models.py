import os
import urllib.parse
import datetime
from typing import Dict, Set

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, SuspiciousOperation
from django.db import models
from django.db.models.query_utils import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(max_length=10, choices=[('M', 'Mężczyzna'), ('F', 'Kobieta'),],
                              null=True, default=None, blank=True)
    school = models.CharField(max_length=100, default="", blank=True)
    matura_exam_year = models.PositiveSmallIntegerField(null=True, default=None, blank=True)
    how_do_you_know_about = models.CharField(max_length=1000, default="", blank=True)
    profile_page = models.TextField(max_length=100000, blank=True, default="")
    cover_letter = models.TextField(max_length=100000, blank=True, default="")
    owncloud_user = models.CharField(max_length=32, blank=True, default="")
    owncloud_password = models.CharField(max_length=32, blank=True, default="")
    k8s_user = models.CharField(max_length=32, blank=True, default="")
    k8s_password = models.CharField(max_length=32, blank=True, default="")

    def is_participating_in(self, year):
        return self.is_participant_in(year) or self.is_lecturer_in(year)

    def is_participant_in(self, year):
        return self.status_for(year) == 'Z'

    def is_lecturer_in(self, year):
        return self.lecturer_workshops.filter(type__year=year, status='Z').exists()

    def all_participation_data(self):
        """
        Returns the participation data from UserWorkshopProfile joined with data about lectures
        """
        participant_data = self.workshop_profile.filter(status__isnull=False)
        lecturer_data = self.lecturer_workshops.filter(status__isnull=False)
        years = set([profile.year for profile in participant_data] + [workshop.type.year for workshop in lecturer_data])
        data = []
        for year in sorted(years):
            profile = next(iter([x for x in participant_data if x.year == year]), None)
            workshops = [x for x in lecturer_data if x.type.year == year]
            status = None
            if profile:
                status = profile.status
            if workshops and status != 'Z':
                status = 'Z' if any([workshop.status == 'Z' for workshop in workshops]) else 'O'
            data.append({'year': year, 'status': status, 'workshops': workshops})
        return data

    def all_participation_years(self) -> Set[int]:
        """
        All years user was qualified or had a lecture
        :return: list of years (integers)
        """
        return self.participant_years().union(self.lecturer_years())

    def participant_years(self) -> Set[int]:
        """
        Years user qualified
        :return: list of years (integers)
        """
        return set([profile.year for profile in self.workshop_profile.filter(status=WorkshopUserProfile.STATUS_ACCEPTED)])

    def lecturer_years(self) -> Set[int]:
        """
        Years user had a lecture
        :return: list of years (integers)
        """
        return set([workshop.type.year for workshop in self.lecturer_workshops.filter(status='Z')])
    
    @property
    def status(self):
        return self.status_for(settings.CURRENT_YEAR)

    def status_for(self, year: int):
        profile = self.workshop_profile_for(year)
        return profile.status if profile else None

    def workshop_profile_for(self, year: int):
        try:
            return self.workshop_profile.filter(year=year).get()
        except WorkshopUserProfile.DoesNotExist:
            return None

    def __str__(self):
        return "{0.first_name} {0.last_name}".format(self.user)

    class Meta:
        permissions = [('see_all_users', 'Can see all users'),
                       ('export_workshop_registration', 'Can download workshop registration data')]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=UserProfile)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.get_or_create(user_profile=instance)


class WorkshopUserProfile(models.Model):
    # for each year
    STATUS_ACCEPTED = 'Z'
    STATUS_REJECTED = 'O'
    STATUS_CHOICES = [
        (STATUS_ACCEPTED, 'Zaakceptowany'),
        (STATUS_REJECTED, 'Odrzucony')
    ]
    user_profile = models.ForeignKey('UserProfile', null=True, related_name='workshop_profile', on_delete=models.CASCADE)

    year = models.IntegerField()
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              null=True, default=None, blank=True)

    def __str__(self):
        return '%s: %s, %s' % (self.year, self.user_profile, self.status)


class PESELField(models.CharField):
    """PESEL field, with checksum verification."""

    def validate(self, pesel: str, user_info: 'UserInfo') -> None:
        super().validate(pesel, user_info)
        # We accept empty PESEL (don't raise exception) for legacy reasons.
        if not pesel:
            return

        # https://en.wikipedia.org/wiki/PESEL#Format
        if len(pesel) != 11:
            raise ValidationError('Długość numeru PESEL jest niepoprawna ({}).'.format(len(pesel)))
        if not pesel.isdigit():
            raise ValidationError('PESEL nie składa się z samych cyfr.')

        pesel_digits = [int(digit) for digit in pesel]
        checksum_mults = [1, 3, 7, 9] * 2 + [1, 3, 1]
        if sum(x*y for x, y in zip(pesel_digits, checksum_mults)) % 10 != 0:
            raise ValidationError('Suma kontrolna PESEL się nie zgadza.')

        if not PESELField._extract_date(pesel):
            raise ValidationError('Data urodzenia zawarta w numerze PESEL nie istnieje.')

    @staticmethod
    def _extract_date(pesel: str) -> datetime.date or None:
        """
        Takes PESEL (string that starts with at least 6 digits) and returns
        birth date associated with it.
        """
        try:
            year, month, day = [int(pesel[i:i+2]) for i in range(0, 6, 2)]
        except ValueError:
            return None
        years_from_month = [1900, 2000, 2100, 2200, 1800]
        count, month = divmod(month, 20)
        year += years_from_month[count]
        try:
            return datetime.date(year, month, day)
        except ValueError:
            return None


POSSIBLE_TSHIRT_SIZES = [
    ('no_idea', 'Nie ogarniam'),
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
]


class UserInfo(models.Model):
    """Info needed for camp, not for qualification."""
    user_profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, related_name='user_info', editable=False)

    pesel = PESELField(max_length=11, blank=True, default="")
    address = models.TextField(max_length=1000, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    tshirt_size = models.CharField(max_length=100, choices=POSSIBLE_TSHIRT_SIZES,
                                   default='no_idea', blank=False, null=False)
    comments = models.CharField(max_length=1000, blank=True, default="")

    class Meta:
        permissions = (('see_user_info', 'Can see user info'),)

    def get_birth_date(self) -> datetime.date or None:
        """
        Retrieves the birth date from the provided PESEL number.
        Returns a date class instance or None if the PESEL is malformed or not present.
        """
        if not self.pesel or len(self.pesel) < 6:
            return None
        return PESELField._extract_date(self.pesel)

    def __str__(self):
        return "{0}".format(self.user_profile)


class ArticleContentHistory(models.Model):
    version = models.IntegerField(editable=False)
    article = models.ForeignKey('Article', null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    modified_by = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    def __str__(self):
        time = '?'
        if self.time:
            time = self.time.strftime('%y-%m-%d %H:%M')
        return '{} (v{} by {} at {})'.format(self.article.name, self.version, self.modified_by, time)

    class Meta:
        unique_together = ('version', 'article',)

    def save(self, *args, **kwargs):
        # start with version 1 and increment it for each version
        current_version = ArticleContentHistory.objects.filter(article=self.article).order_by('-version')[:1]
        self.version = current_version[0].version + 1 if current_version else 1
        self.modified_by = self.article.modified_by
        super(ArticleContentHistory, self).save(*args, **kwargs)


class Article(models.Model):
    name = models.SlugField(max_length=50, null=False, blank=False, unique=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=100000, blank=True)
    modified_by = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_NULL)
    on_menubar = models.BooleanField(default=False)

    class Meta:
        permissions = (('can_put_on_menubar', 'Can put on menubar'),)

    def content_history(self):
        return ArticleContentHistory.objects.filter(article=self).order_by('-version')

    def __str__(self):
        return '{} "{}"'.format(self.name, self.title)

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        # save summary history
        content_history = self.content_history()
        if not content_history or self.content != content_history[0].content:
            new_content = ArticleContentHistory(article=self, content=self.content)
            new_content.save()


class WorkshopCategory(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        unique_together = ('year', 'name',)

    def __str__(self):
        return '%d: %s' % (self.year, self.name)


class WorkshopType(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        unique_together = ('year', 'name',)

    def __str__(self):
        return '%d: %s' % (self.year, self.name)


class Workshop(models.Model):
    """
    Workshop taking place during a specific workshop/year
    """
    STATUS_ACCEPTED = 'Z'
    STATUS_REJECTED = 'O'
    STATUS_CANCELLED = 'X'
    STATUS_CHOICES = [
        (STATUS_ACCEPTED, 'Zaakceptowane'),
        (STATUS_REJECTED, 'Odrzucone'),
        (STATUS_CANCELLED, 'Odwołane')
    ]

    name = models.SlugField(max_length=50, null=False, blank=False, unique=True)
    title = models.CharField(max_length=50)
    proposition_description = models.TextField(max_length=100000, blank=True)
    type = models.ForeignKey(WorkshopType, on_delete=models.PROTECT, null=False)
    category = models.ManyToManyField(WorkshopCategory, blank=True)
    lecturer = models.ManyToManyField(UserProfile, blank=True, related_name='lecturer_workshops')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              null=True, default=None, blank=True)
    page_content = models.TextField(max_length=100000, blank=True)
    page_content_is_public = models.BooleanField(default=False)

    is_qualifying = models.BooleanField(default=True)
    qualification_problems = models.FileField(null=True, blank=True, upload_to="qualification")
    participants = models.ManyToManyField(UserProfile, blank=True, related_name='workshops', through='WorkshopParticipant')
    qualification_threshold = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)
    max_points = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)

    def is_workshop_editable(self) -> bool:
        return not hasattr(self, 'type') or self.type.year == settings.CURRENT_YEAR

    def is_qualification_editable(self) -> bool:
        return self.is_workshop_editable() and datetime.datetime.now().date() < settings.WORKSHOPS_START_DATE

    def clean(self):
        super(Workshop, self).clean()
        if self.max_points is None and self.qualification_threshold is not None:
            raise ValidationError('Maksymalna liczba punktów musi być ustawiona jeśli próg kwalifikacji jest ustawiony')

    class Meta:
        permissions = (('see_all_workshops', 'Can see all workshops'),)

    def __str__(self):
        return str(self.type.year) + ': ' + (' (' + self.status + ') ' if self.status else '') + self.title

    """
    Retrieve information needed to display a meaningful link to the workshop page
    """
    def info_for_client_link(self) -> Dict[str, str]:
        return {'name': self.name, 'title': str(self.title)}

    def registered_count(self):
        return self.workshopparticipant_set.count()

    def qualified_count(self):
        if self.qualification_threshold is None:
            return None
        return self.workshopparticipant_set.filter(qualification_result__gte=self.qualification_threshold).count()

    """
    Should the workshop be publicly visible? (accepted or cancelled)
    """
    def is_publicly_visible(self):
        return self.status == 'Z' or self.status == 'X'


class WorkshopParticipant(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    participant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    qualification_result = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)
    comment = models.CharField(max_length=1000, null=True, default=None, blank=True)

    def is_qualified(self):
        threshold = self.workshop.qualification_threshold
        if threshold is None or self.qualification_result is None:
            return None
        if self.qualification_result >= threshold:
            return True
        else:
            return False

    def result_in_percent(self):
        if self.qualification_result is None:
            return None
        max_points = self.workshop.max_points
        if max_points is None:
            max_points = self.workshop.workshopparticipant_set.aggregate(max_points=models.Max('qualification_result'))['max_points']
        return max(min(self.qualification_result / max_points * 100, settings.MAX_POINTS_PERCENT), 0)

    class Meta:
        unique_together = [('workshop', 'participant')]


class ResourceYearPermission(models.Model):
    """
    Resource associated with a WWW edition (year). Resource can be accessed by
    users who qualified or had a lecture on year. User is granted access to
    root_url and recursively to all files and subdirectories inside.
    """
    display_name = models.CharField(max_length=50, blank=True)
    access_url = models.URLField(blank=True,
                                 help_text="URL dla przycisku w menu. Przycisk nie jest wyświetlany jeśli url jest pusty")
    root_path = models.CharField(max_length=256, null=False, blank=False,
                                 help_text='bez "/" na końcu. np. "/internety/www15"')
    year = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return "{} - {}".format(self.year,
                                self.display_name if self.display_name != "" else self.root_path)

    def clean(self):
        super().clean()
        if self.access_url != "" and self.display_name == "":
            raise ValidationError("Wyświetlana nazwa musi być ustawiona jeśli "
                                  "URL dostępu jest ustawiony")

        if self.root_path.endswith("/"):
            self.root_path = self.root_path[:-1]
        if not self.root_path.startswith("/"):
            self.root_path = "/" + self.root_path

    @staticmethod
    def resources_for_uri(uri: str):
        scheme, netloc, path, query, fragment = urllib.parse.urlsplit(uri)
        path = os.path.normpath(path)  # normalize path
        path_parts = path.split('/')
        if path_parts[0] != "":
            raise SuspiciousOperation("Path has to start with /")
        path_parts = path_parts[1:]

        query = Q(pk__isnull=True)  # always false
        for i in range(len(path_parts)+1):
            query |= Q(root_path='/'+'/'.join(path_parts[:i]))

        # We check all root_url that are prefixes of received url
        return ResourceYearPermission.objects.filter(query)

    class Meta:
        permissions = [('access_all_resources', 'Access all resources'), ]
        ordering = ['year', 'display_name']
