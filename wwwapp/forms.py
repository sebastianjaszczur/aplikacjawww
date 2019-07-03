#-*- coding: utf-8 -*-
from django.forms import ModelForm, FileInput, FileField
from django.contrib.auth.models import User
from django.forms import ModelChoiceField, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper

from django_select2.forms import Select2MultipleWidget, Select2Widget

from .models import UserProfile, Article, Workshop, WorkshopCategory, WorkshopType, UserInfo
from .widgets import RichTextarea

from . import settings

class UserProfilePageForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_page']
        labels = {'profile_page': "Strona profilowa"}
        widgets = {'profile_page': RichTextarea()}


class UserCoverLetterForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cover_letter']
        labels = {'cover_letter': "List motywacyjny"}
        widgets = {'cover_letter': RichTextarea()}


class UserInfoPageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserInfoPageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
    
    class Meta:
        model = UserInfo
        fields = ['pesel', 'address', 'start_date', 'end_date', 'meeting_point',
                  'tshirt_size', 'comments']
        labels = {
            'pesel': 'Pesel',
            'address': 'Adres zameldowania',
            'start_date': 'Data przyjazdu :-)',
            'end_date': 'Data wyjazdju :-(',
            'meeting_point': 'Miejsce zbiórki',
            'tshirt_size': 'Rozmiar koszulki',
            'comments': 'Dodatkowe uwagi (np. wegetarianin, uczulony na X, ale też inne)',
        }


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
    
    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'matura_exam_year', 'how_do_you_know_about']
        labels = {
            'gender': 'Płeć',
            'school': 'Szkoła lub uniwersytet',
            'matura_exam_year': 'Rok zdania matury',
            'how_do_you_know_about': 'Skąd wiesz o WWW?',
        }


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'E-mail',
        }


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'name', 'on_menubar', 'content']
        labels = {
            'title': 'Tytuł',
            'name': 'Nazwa (w URLach)',
            'on_menubar': 'Umieść w menu',
            'content': 'Treść',
        }
        widgets = {
            'content': RichTextarea()
        }

    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        if not user.has_perm('wwwapp.can_put_on_menubar'):
            del self.fields['on_menubar']


class WorkshopForm(ModelForm):
    category = ModelMultipleChoiceField(label="Kategorie", queryset=WorkshopCategory.objects.filter(year=settings.CURRENT_YEAR),
                                         required=False, widget=Select2MultipleWidget(attrs={'width': '200px'}))

    category.help_text = ""  # this removes annoying message ' Hold down "Control", or "Command" (..) '
    type = ModelChoiceField(label="Rodzaj zajęć", queryset=WorkshopType.objects.filter(year=settings.CURRENT_YEAR), required=False,
                             widget=Select2Widget(attrs={'width': '200px'}))

    class Meta:
        model = Workshop
        fields = ['title', 'name', 'type', 'category', 'proposition_description']
        widgets = {
            'proposition_description': RichTextarea()
        }
        labels = {
            'title': 'Tytuł',
            'name': 'Nazwa (w URLach)',
            'proposition_description': 'Opis propozycji warsztatów',
        }


class WorkshopPageForm(ModelForm):
    qualification_problems = FileField(required=False, widget=FileInput())

    class Meta:
        model = Workshop
        fields = ['qualification_problems', 'is_qualifying', 'page_content_is_public', 'qualification_threshold', 'page_content']
        widgets = {
            'page_content': RichTextarea(),
        }
        labels = {
            'qualification_problems': 'Zadania kwalifikacyjne w PDF:',
            'is_qualifying': 'Czy warsztaty są kwalifikujące (odznacz, jeśli nie zamierzasz dodawać zadań i robić kwalifikacji)',
            'page_content': 'Strona warsztatów',
            'page_content_is_public': 'Zaznacz, jeśli opis jest gotowy i może już być publiczny.',
            'qualification_threshold': 'Minimalna liczba punktów potrzeba do kwalifikacji (wpisz dopiero po sprawdzeniu zadań)'
        }
