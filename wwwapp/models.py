from django.db import models
from sanitizer.models import SanitizedTextField
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
    content = SanitizedTextField(max_length=100000, strip=True)


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'content']
