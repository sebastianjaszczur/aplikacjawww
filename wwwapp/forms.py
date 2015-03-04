#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User

from wwwapp.models import UserProfile, Article


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender']
        labels = {
            'gender': u'Płeć',
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': u'Imię',
            'last_name': u'Nazwisko',
            'email': u'E-mail',
        }


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'content']
