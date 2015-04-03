#-*- coding: utf-8 -*-
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.html import format_html
from django.utils.encoding import force_text

from wwwapp.models import Article


DEFAULT_CONFIG = {
    'language': 'pl',
    'removePlugins': 'link',
    'extraPlugins': 'linklocal',
    'linklocal_autocomplete': '/articleNameList',
    'linklocal_prefix': '/article/',
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
