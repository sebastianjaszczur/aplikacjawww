#-*- coding: utf-8 -*-
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.html import format_html
from django.utils.encoding import force_text

DEFAULT_CONFIG = {
    'language': 'pl',
    'removePlugins': 'link,scayt,contextmenu,liststyle,tabletools,forms,language,print,preview,newpage,bidi,flash,iframe,templates',
    # contextmenu is removed, because it's annoying (and it replaces better browser contextmenu)
    # scayt,liststyle,tabletools are removed, because they require contextmenu
    # forms is removed, because there is no use-case for it
    # language is removed, because it's useless (it sets language of content, by the way)
    # print,preview,newpage are removed, because they're useless
    # bidi is removed, because it's completely useless (it changes direction of text)
    # flash,iframe are removed, because they're dangerous
    # templates are useless, unless someone defines better ones
    'extraPlugins': 'linklocal,footnotes',
    'disableNativeSpellChecker': False,  # browser spellchecker is better
    'linklocal_autocomplete': '/articleNameList',
    'linklocal_prefix': '/article/',
    'format_tags': 'p;h2;h3;h4',
}


class RichTextarea(Widget):
    def __init__(self, attrs=None):
        self.config = DEFAULT_CONFIG.copy()
        config = DjangoJSONEncoder().encode(self.config)
        default_attrs = {'data-ckeditor-config': config }
        if attrs:
            default_attrs.update(attrs)
        super(RichTextarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return format_html(u'<textarea{}>\r\n{}</textarea>',
                           flatatt(final_attrs),
                           force_text(value))
