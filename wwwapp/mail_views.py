#-*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect, render

from models import User, Workshop, UserProfile
from views import get_context


_registered_filters = dict()


def _register_as_email_filter(filter_id, name):
    def decorator(method):
        if filter_id in _registered_filters and _registered_filters[filter_id] != method:
            raise NameError("Filter '{}' already registered!".format(name))
        _registered_filters[filter_id] = (method, name)
        return method
    return decorator


@_register_as_email_filter('all', u'wszyscy')
def _all():
    return User.objects.all()


@_register_as_email_filter('none', u'nikt')
def _none():
    return None


def _get_user_objects_of_lecturers_of_workshops(workshops):
    users = set()
    for workshop in workshops:
        for user_profile in workshop.lecturer.all():
            users.add(user_profile.user)
    return users


@_register_as_email_filter('allLecturers', u'wszyscy prowadzący')
def _all_lecturers():
    all_workshops = Workshop.objects.all()
    return _get_user_objects_of_lecturers_of_workshops(all_workshops)


@_register_as_email_filter('acceptedLecturers', u'prowadzący zaakceptowanych warsztatów')
def _accepted_lecturers():
    accepted_workshops = Workshop.objects.filter(status='Z')
    return _get_user_objects_of_lecturers_of_workshops(accepted_workshops)


@_register_as_email_filter('deniedLecturers', u'prowadzący odrzuconych warsztatów')
def _denied_lecturers():
    denied_workshops = Workshop.objects.filter(status='O')
    return _get_user_objects_of_lecturers_of_workshops(denied_workshops)


@_register_as_email_filter('allParticipants', u'wszyscy uczestnicy zapisani na co najmniej jeden warsztat')
def _all_participants():
    all_workshops = Workshop.objects.all()
    participants = set()
    for workshop in all_workshops:
        for participant in workshop.participants.all():
            participants.add(participant.user)
    return participants


@_register_as_email_filter('allQualified', u'wszyscy uczestnicy o statusie zakwalifikowanym')
def _all_qualified():
    return [ profile.user for profile in UserProfile.objects.all() if profile.status == 'Z' ]


@_register_as_email_filter('allRefused', u'wszyscy uczestnicy o statusie odrzuconym')
def _all_refused():
    return [ profile.user for profile in UserProfile.objects.all() if profile.status == 'O' ]


def filtered_emails(request, filter_id=''):
    if not request.user.has_perm('wwwapp.see_all_users'):
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
