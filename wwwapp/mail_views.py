#-*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect, render

from wwwapp.models import User
from wwwapp.views import get_context


_registered_filters = dict()


def _register_as_email_filter(filter_id, name):
    def decorator(method):
        if filter_id in _registered_filters and _registered_filters[filter_id] != method:
            raise NameError("Filter '{}' already registered!".format(name))
        _registered_filters[filter_id] = (method, name)
        return method
    return decorator


@_register_as_email_filter('all', 'wszyscy')
def _filter1():
    return User.objects.all()


@_register_as_email_filter('none', 'nikt')
def _filter1():
    return None


def filtered_emails(request, filter_id=''):
    if not request.user.has_perm('user_profiles.can_see_all_users'):
        return redirect('login')

    context = get_context(request)
    context['title'] = u'Filtrowane emaile użytkowników'
    context['filtered_users'] = None
    if filter_id in _registered_filters:
        method, name = _registered_filters[filter_id]
        context['filter_name'] = name
        context['filtered_users'] = method()
        if not context['filtered_users']:
            messages.info(request, u'Nie znaleziono użytkowników spełniających kryteria!')

    context['filter_methods'] = [
        (filter_id, _registered_filters[filter_id][1]) for filter_id in _registered_filters.iterkeys()
    ]

    return render(request, 'filteredEmails.html', context)
