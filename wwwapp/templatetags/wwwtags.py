# coding=utf-8
from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter
def qualified_mark(value):
    if value is None:
        return mark_safe('<span class="maybe-qualified">?</span>')
    elif value is True:
        return mark_safe('<span class="qualified">✔</span> TAK')
    else:
        return mark_safe('<span class="not-qualified">✘</span> NIE')
