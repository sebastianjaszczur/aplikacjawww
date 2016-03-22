#-*- coding: utf-8 -*-
from django.forms import ModelForm, FileInput, FileField
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper

from django_select2 import ModelSelect2MultipleField, Select2MultipleWidget, ModelSelect2Field, Select2Widget

from .models import UserProfile, Article, Workshop, WorkshopCategory, WorkshopType, UserInfo
from .widgets import RichTextarea

from . import settings

class UserProfilePageForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_page']
        labels = {'profile_page': u"Strona profilowa"}
        widgets = {'profile_page': RichTextarea()}


class UserCoverLetterForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cover_letter']
        labels = {'cover_letter': u"List motywacyjny"}
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
            'pesel': u'Pesel',
            'address': u'Adres zameldowania (potrzebny nam do ubezpieczenia)',
            'start_date': u'Data przyjazdu :-)',
            'end_date': u'Data wyjazdju :-(',
            'meeting_point': u'Miejsce zbiórki',
            'tshirt_size': u'Rozmiar koszulki',
            'comments': u'Dodatkowe uwagi (np. wegetarianin, uczulony na X, ale też inne)',
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
            'gender': u'Płeć',
            'school': u'Szkoła lub uniwersytet',
            'matura_exam_year': u'Rok zdania matury',
            'how_do_you_know_about': u'Skąd wiesz o WWW?',
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
            'first_name': u'Imię',
            'last_name': u'Nazwisko',
            'email': u'E-mail',
        }


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'name', 'on_menubar', 'content']
        labels = {
            'title': u'Tytuł',
            'name': u'Nazwa (w URLach)',
            'on_menubar': u'Umieść w menu',
            'content': u'Treść',
        }
        widgets = {
            'content': RichTextarea()
        }

    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        if not user.has_perm('wwwapp.can_put_on_menubar'):
            del self.fields['on_menubar']


class WorkshopForm(ModelForm):
    category = ModelSelect2MultipleField(label="Kategorie", queryset=WorkshopCategory.objects.filter(year=settings.CURRENT_YEAR),
                                         required=False, widget=Select2MultipleWidget(select2_options={'width': '200px'}))

    category.help_text = ""  # this removes annoying message ' Hold down "Control", or "Command" (..) '
    type = ModelSelect2Field(label="Rodzaj zajęć", queryset=WorkshopType.objects.filter(year=settings.CURRENT_YEAR), required=False,
                             widget=Select2Widget(select2_options={'width': '200px'}))

    class Meta:
        model = Workshop
        fields = ['title', 'name', 'type', 'category', 'proposition_description']
        widgets = {
            'proposition_description': RichTextarea()
        }
        labels = {
            'title': u'Tytuł',
            'name': u'Nazwa (w URLach)',
            'proposition_description': u'Opis propozycji warsztatów',
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
            'qualification_problems': u'Zadania kwalifikacyjne w PDF:',
            'is_qualifying': u'Czy warsztaty są kwalifikujące (odznacz, jeśli nie zamierzasz dodawać zadań i robić kwalifikacji)',
            'page_content': u'Strona warsztatów',
            'page_content_is_public': u'Zaznacz, jeśli opis jest gotowy i może już być publiczny.',
            'qualification_threshold': u'Minimalna liczba punktów potrzeba do kwalifikacji (wpisz dopiero po sprawdzeniu zadań)'
        }
