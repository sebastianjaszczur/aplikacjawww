from django.db import models
from django.db.models import TextField, BooleanField, CharField
from django.forms import ModelForm
import re
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    gender = CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'),],
                       null=True, default=None, blank=False)
    just_registered = BooleanField(default=True)

    def __unicode__(self):
        return self.user.username

class AlphaNumericField(models.CharField):
    def clean(self, value, model_instance):
        value = super(AlphaNumericField, self).clean(value, model_instance)
        if not re.match(r'[A-z0-9]+', value):
            raise ValidationError('AlphaNumeric characters only.')
        return value


class Article(models.Model):
    name = AlphaNumericField(max_length=40, null=False)
    content = TextField(max_length=100000, blank=True)
    
    on_menubar = BooleanField(default=False)
    
    def __unicode__(self):
        return self.name


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'content']
