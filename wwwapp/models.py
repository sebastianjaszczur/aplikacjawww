#-*- coding: utf-8 -*-
from django.db import models

import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from wwwapp import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_info = models.OneToOneField('UserInfo')

    gender = models.CharField(max_length=10, choices=[('M', u'Mężczyzna'), ('F', u'Kobieta'),],
                              null=True, default=None, blank=True)
    school = models.CharField(max_length=100, default="", blank=True)
    matura_exam_year = models.PositiveSmallIntegerField(null=True, default=None, blank=True)
    how_do_you_know_about = models.CharField(max_length=1000, default="", blank=True)
    profile_page = models.TextField(max_length=100000, blank=True, default="")
    cover_letter = models.TextField(max_length=100000, blank=True, default="")

    @property
    def status(self):
        return self.status_for(settings.CURRENT_YEAR)

    def status_for(self, year):
        try:
            return self.workshop_profile.filter(year=year).get().status
        except WorkshopUserProfile.DoesNotExist:
            return None

    def __unicode__(self):
        return u"{0.first_name} {0.last_name}".format(self.user)

    class Meta:
        permissions = (('see_all_users', u'Can see all users'),)

class WorkshopUserProfile(models.Model):
    # for each year
    user_profile = models.ForeignKey('UserProfile', null=True, related_name='workshop_profile')

    year = models.IntegerField()
    status = models.CharField(max_length=10,
                              choices=[('Z', u'Zaakceptowany'), ('O', u'Odrzucony')],
                              null=True, default=None, blank=True)

    def __unicode__(self):
        return u'%s: %s, %s' % (self.year, self.user_profile, self.status)

# That's bad, one year design. I'm so sorry.
POSSIBLE_DATES = [
    ('no_idea', u'Nie ogarniam'),
] + [(unicode(day_number), unicode(day_number) + u' sierpien') for day_number in xrange(17, 29)]

# The same
POSSIBLE_PLACES = [
    ('no_idea', u'Nie ogarniam'),
    ('wierchomla', u'Wierchomla Wielka'),
    ('warsaw', u'Warszawa'),
    ('cracow', u'Kraków')
]

POSSIBLE_TSHIRT_SIZES = [
    ('no_idea', u'Nie ogarniam'),
    ("XS", u"XS"),
    ("S", u"S"),
    ("M", u"M"),
    ("L", u"L"),
    ("XL", u"XL"),
    ("XXL", u"XXL"),
]


class UserInfo(models.Model):
    """Info needed for camp, not for qualification."""
    pesel = models.CharField(max_length=20, blank=True, default="")
    address = models.TextField(max_length=1000, blank=True, default="")
    start_date = models.CharField(max_length=100, choices=POSSIBLE_DATES,
                                  default='no_idea', blank=False, null=False)
    end_date = models.CharField(max_length=100, choices=POSSIBLE_DATES,
                                default='no_idea', blank=False, null=False)
    meeting_point = models.CharField(max_length=100, choices=POSSIBLE_PLACES,
                                     default='no_idea', blank=False, null=False)
    tshirt_size = models.CharField(max_length=100, choices=POSSIBLE_TSHIRT_SIZES,
                                     default='no_idea', blank=False, null=False)
    comments = models.CharField(max_length=1000, blank=True, default="")
    
    class Meta:
        permissions = (('see_user_info', u'Can see user info'),)


class AlphaNumericField(models.CharField):
    def clean(self, value, model_instance):
        value = super(AlphaNumericField, self).clean(value, model_instance)
        if not re.match(r'[A-z0-9]+', value):
            raise ValidationError('AlphaNumeric characters only.')
        return value


class ArticleContentHistory(models.Model):
    version = models.IntegerField(editable=False)
    article = models.ForeignKey('Article')
    content = models.TextField()
    modified_by = models.ForeignKey(User, null=True, default=None)
    time = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    def __unicode__(self):
        time = u'?'
        if self.time:
            time = self.time.strftime(u'%y-%m-%d %H:%M')
        return u'{} (v{} by {} at {})'.format(self.article.name, self.version, self.modified_by, time)

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
    modified_by = models.ForeignKey(User, null=True, default=None)
    on_menubar = models.BooleanField(default=False)

    class Meta:
        permissions = (('can_put_on_menubar', u'Can put on menubar'),)

    def content_history(self):
        return ArticleContentHistory.objects.filter(article=self).order_by('-version')

    def __unicode__(self):
        return u'{} "{}"'.format(self.name, self.title)

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        # save summary history
        content_history = self.content_history()
        if not content_history or self.content != content_history[0].content:
            newContent = ArticleContentHistory(article=self, content=self.content)
            newContent.save()


class WorkshopCategory(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        unique_together = ('year', 'name',)

    def __unicode__(self):
        return '%d: %s' % (self.year, self.name)


class WorkshopType(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        unique_together = ('year', 'name',)

    def __unicode__(self):
        return '%d: %s' % (self.year, self.name)


class Workshop(models.Model):
    name = models.SlugField(max_length=50, null=False, blank=False, unique=True)
    title = models.CharField(max_length=50, null=True, blank=False)
    proposition_description = models.TextField(max_length=100000, blank=True)
    type = models.ForeignKey(WorkshopType, null=True, blank=True, default=None)
    category = models.ManyToManyField(WorkshopCategory, blank=True)
    lecturer = models.ManyToManyField(UserProfile, blank=True)
    status = models.CharField(max_length=10,
                              choices=[('Z', u'Zaakceptowane'), ('O', u'Odrzucone')],
                              null=True, default=None, blank=True)
    page_content = models.TextField(max_length=100000, blank=True)
    page_content_is_public = models.BooleanField(default=False)

    is_qualifying = models.BooleanField(default=True)
    qualification_problems = models.FileField(null=True, blank=True, upload_to="qualification")
    participants = models.ManyToManyField(UserProfile, blank=True, related_name='workshops', through='WorkshopParticipant')
    qualification_threshold = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)

    def clean(self):
        if self.type.year != settings.CURRENT_YEAR:
            raise ValidationError('cannot edit workshops from previous years')

    class Meta:
        permissions = (('see_all_workshops', u'Can see all workshops'),)

    def __unicode__(self):
        return str(self.type.year) + ': ' + (' (' + self.status + ') ' if self.status else '') + self.title


class WorkshopParticipant(models.Model):
    workshop = models.ForeignKey(Workshop)
    participant = models.ForeignKey(UserProfile)

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

    class Meta:
        unique_together = [('workshop', 'participant')]
