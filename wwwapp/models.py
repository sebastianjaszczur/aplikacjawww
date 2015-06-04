#-*- coding: utf-8 -*-
from django.db import models

import re
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    gender = models.CharField(max_length=10, choices=[('M', u'Mężczyzna'), ('F', u'Kobieta'),],
                       null=True, default=None, blank=True)
    school = models.CharField(max_length=100, default="", blank=True)
    matura_exam_year = models.PositiveSmallIntegerField(null=True, default=None, blank=True)
    how_do_you_know_about = models.CharField(max_length=1000, default="", blank=True)
    profile_page = models.TextField(max_length=100000, blank=True, default="")

    def __unicode__(self):
        return "{0.first_name} {0.last_name}".format(self.user)
    
    class Meta:
        permissions = (('see_all_users', u'Can see all users'),)


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
        if (self.time):
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
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    
    def __unicode__(self):
        return self.name


class WorkshopType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    
    def __unicode__(self):
        return self.name


class Workshop(models.Model):
    name = models.SlugField(max_length=50, null=False, blank=False, unique=True)
    title = models.CharField(max_length=50, null=True, blank=False)
    proposition_description = models.TextField(max_length=100000, blank=True)
    type = models.ForeignKey(WorkshopType, null=True, default=None)
    category = models.ManyToManyField(WorkshopCategory, blank=True)
    lecturer = models.ManyToManyField(UserProfile, blank=True)
    status = models.CharField(max_length=10, choices=[('Z', u'Zaakceptowane'), ('O', u'Odrzucone'),],
                              null=True, default=None, blank=True)
    page_content = models.TextField(max_length=100000, blank=True)
    page_content_is_public = models.BooleanField(default=False)
    
    qualification_problems = models.FileField(null=True, upload_to="qualification")
    participants = models.ManyToManyField(UserProfile, blank=True, related_name='+')
    
    class Meta:
        permissions = (('see_all_workshops', u'Can see all workshops'),)
    
    def __unicode__(self):
        return (self.status + ":" if self.status else "") + self.title
