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


@register.filter
def question_mark_on_none_value(value):
    if value is None:
        return mark_safe('<span class="maybe-qualified">?</span>')
    return value


@register.filter
def question_mark_on_empty_string(value):
    if value == '':
        return '?'
    return value
