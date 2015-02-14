from django.db import models
from django.db.models import TextField, BooleanField, CharField, ForeignKey
from django.forms import ModelForm
import re
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    gender = CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'),],
                       null=True, default=None, blank=False)

    def __unicode__(self):
        return self.user.username

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
    modified_by = ForeignKey(User, null=True, default=None)

    class Meta:
        unique_together = ('version', 'article',)

    def save(self, *args, **kwargs):
        # start with version 1 and increment it for each version
        current_version = ArticleContentHistory.objects.filter(article=self.article).order_by('-version')[:1]
        self.version = current_version[0].version + 1 if current_version else 1
        self.modified_by = self.article.modified_by
        super(ArticleContentHistory, self).save(*args, **kwargs)


class Article(models.Model):
    name = AlphaNumericField(max_length=40, null=False)
    content = TextField(max_length=100000, blank=True)
    modified_by = ForeignKey(User, null=True, default=None)
    on_menubar = BooleanField(default=False)
    
    def content_history(self):
        return ArticleContentHistory.objects.filter(article=self).order_by('-version')
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        # save summary history
        content_history = self.content_history()
        if not content_history or self.content != content_history[0].content:
            newContent = ArticleContentHistory(article=self, content=self.content)
            newContent.save()


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'content']
