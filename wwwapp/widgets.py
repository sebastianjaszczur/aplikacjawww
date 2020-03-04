from django.forms.widgets import Widget
from django.template import Template, Context


class RenderHTML(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return Template("{% load bleach_tags %} {{ x|bleach }}").render(Context({'x': value}))
