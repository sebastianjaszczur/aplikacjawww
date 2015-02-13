from django.db import models
from django.db.models import TextField
from django.forms import ModelForm
import re


class AlphaNumericField(models.CharField):
    def clean(self, value, model_instance):
        value = super(AlphaNumericField, self).clean(value, model_instance)
        if not re.match(r'[A-z0-9]+', value):
            raise ValidationError('AlphaNumeric characters only.')
        return value


class Article(models.Model):
    name = AlphaNumericField(max_length=40, null=False)
    content = TextField(max_length=100000)


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'content']
