import re
from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_info = models.OneToOneField('UserInfo', on_delete=models.CASCADE)

    gender = models.CharField(max_length=10, choices=[('M', 'Mężczyzna'), ('F', 'Kobieta'),],
                              null=True, default=None, blank=True)
    school = models.CharField(max_length=100, default="", blank=True)
    matura_exam_year = models.PositiveSmallIntegerField(null=True, default=None, blank=True)
    how_do_you_know_about = models.CharField(max_length=1000, default="", blank=True)
    profile_page = models.TextField(max_length=100000, blank=True, default="")
    cover_letter = models.TextField(max_length=100000, blank=True, default="")

    def is_participating_in(self, year):
        return self.status_for(year) == 'Z' \
               or Workshop.objects.filter(type__year=year, lecturer=self, status='Z').exists()
    
    @property
    def status(self):
        return self.status_for(settings.CURRENT_YEAR)

    def status_for(self, year):
        try:
            return self.workshop_profile.filter(year=year).get().status
        except WorkshopUserProfile.DoesNotExist:
            return None

    def __str__(self):
        return "{0.first_name} {0.last_name}".format(self.user)

    class Meta:
        permissions = [('see_all_users', 'Can see all users'),
                       ('export_workshop_registration', 'Can download workshop registration data')]


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
    def _extract_date(pesel: str) -> date or None:
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
            return date(year, month, day)
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

    def get_birth_date(self) -> date or None:
        """
        Retrieves the birth date from the provided PESEL number.
        Returns a date class instance or None if the PESEL is malformed or not present.
        """
        if not self.pesel or len(self.pesel) < 6:
            return None
        return PESELField._extract_date(self.pesel)


class AlphaNumericField(models.CharField):
    def clean(self, value, model_instance):
        value = super(AlphaNumericField, self).clean(value, model_instance)
        if not re.match(r'[A-z0-9]+', value):
            raise ValidationError('AlphaNumeric characters only.')
        return value


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
    name = models.SlugField(max_length=50, null=False, blank=False, unique=True)
    title = models.CharField(max_length=50)
    proposition_description = models.TextField(max_length=100000, blank=True)
    type = models.ForeignKey(WorkshopType, on_delete=models.PROTECT, null=False)
    category = models.ManyToManyField(WorkshopCategory, blank=True)
    lecturer = models.ManyToManyField(UserProfile, blank=True)
    status = models.CharField(max_length=10,
                              choices=[('Z', 'Zaakceptowane'), ('O', 'Odrzucone'), ('X', 'Odwołane')],
                              null=True, default=None, blank=True)
    page_content = models.TextField(max_length=100000, blank=True)
    page_content_is_public = models.BooleanField(default=False)

    is_qualifying = models.BooleanField(default=True)
    qualification_problems = models.FileField(null=True, blank=True, upload_to="qualification")
    participants = models.ManyToManyField(UserProfile, blank=True, related_name='workshops', through='WorkshopParticipant')
    qualification_threshold = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)
    max_points = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)

    def clean(self):
        super(Workshop, self).clean()
        if self.type.year != settings.CURRENT_YEAR:
            raise ValidationError('Nie można edytować warsztatów z poprzednich lat')
        if self.max_points is None and self.qualification_threshold is not None:
            raise ValidationError('Maksymalna liczba punktów musi być ustawiona jeśli próg kwalifikacji jest ustawiony')

    class Meta:
        permissions = (('see_all_workshops', 'Can see all workshops'),)

    def __str__(self):
        return str(self.type.year) + ': ' + (' (' + self.status + ') ' if self.status else '') + self.title

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
        return min(self.qualification_result / max_points * 100, settings.MAX_POINTS_PERCENT)

    class Meta:
        unique_together = [('workshop', 'participant')]
