#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User

from wwwapp.models import UserProfile, Article, Workshop


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'matura_exam_year', 'how_do_you_know_about', 'interests']
        labels = {
            'gender': u'Płeć',
            'school': u'Szkoła lub uniwersytet',
            'matura_exam_year': u'Rok zdania matury',
            'how_do_you_know_about': u'Skąd wiesz o WWW?',
            'interests': 'Zainteresowania',
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


class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop
        fields = ['name', 'proposition_description', 'category']
