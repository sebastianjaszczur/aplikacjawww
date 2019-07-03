#-*- coding: utf-8 -*-
from datetime import date
from django.contrib import messages
from django.shortcuts import redirect, render
from django.conf import settings

from .models import Workshop, WorkshopUserProfile
from .views import get_context


_registered_filters = dict()


def _register_as_email_filter(filter_id, name):
    def decorator(method):
        if filter_id in _registered_filters and _registered_filters[filter_id] != method:
            raise NameError("Filter '{}' already registered!".format(name))
        _registered_filters[filter_id] = (method, name)
        return method
    return decorator


@_register_as_email_filter('all', 'wszyscy (uczestnicy zapisani na co najmniej jeden warsztat oraz prowadzący)')
def _all(year):
    return _all_participants(year) | _all_lecturers(year)


def _get_user_objects_of_lecturers_of_workshops(workshops):
    users = set()
    for workshop in workshops:
        for user_profile in workshop.lecturer.all():
            users.add(user_profile.user)
    return users


@_register_as_email_filter('allLecturers', 'wszyscy prowadzący')
def _all_lecturers(year):
    all_workshops = Workshop.objects.filter(type__year=year)
    return _get_user_objects_of_lecturers_of_workshops(all_workshops)


@_register_as_email_filter('acceptedLecturers', 'prowadzący zaakceptowanych warsztatów')
def _accepted_lecturers(year):
    accepted_workshops = Workshop.objects.filter(status='Z', type__year=year)
    return _get_user_objects_of_lecturers_of_workshops(accepted_workshops)


@_register_as_email_filter('deniedLecturers', 'prowadzący odrzuconych warsztatów')
def _denied_lecturers(year):
    denied_workshops = Workshop.objects.filter(status='O', type__year=year)
    return _get_user_objects_of_lecturers_of_workshops(denied_workshops)


@_register_as_email_filter('allParticipants', 'wszyscy uczestnicy zapisani na co najmniej jeden warsztat')
def _all_participants(year):
    all_workshops = Workshop.objects.filter(type__year=year)
    participants = set()
    for workshop in all_workshops:
        for participant in workshop.participants.all():
            participants.add(participant.user)
    return participants


@_register_as_email_filter('allQualified', 'wszyscy uczestnicy o statusie zakwalifikowanym')
def _all_qualified(year):
    return [profile.user_profile.user for profile in
            WorkshopUserProfile.objects.filter(year=year) if profile.status == 'Z']


@_register_as_email_filter('allRefused', 'wszyscy uczestnicy o statusie odrzuconym')
def _all_refused(year):
    return [profile.user_profile.user for profile in
            WorkshopUserProfile.objects.filter(year=year) if profile.status == 'O']


def filtered_emails(request, year='0', filter_id=''):
    if not request.user.has_perm('wwwapp.see_all_users'):
        return redirect('login')

    year = int(year or settings.CURRENT_YEAR)
    context = get_context(request)
    context['title'] = 'Filtrowane emaile użytkowników'
    context['filtered_users'] = None
    if filter_id in _registered_filters:
        method, name = _registered_filters[filter_id]
        context['chosen_filter_name'] = name
        context['chosen_year'] = year
        context['filtered_users'] = method(year)
        if not context['filtered_users']:
            messages.info(request, 'Nie znaleziono użytkowników spełniających kryteria!')

    context['filter_methods'] = [
        (filter_id, _registered_filters[filter_id][1]) for filter_id in _registered_filters.keys()
    ]
    context['years'] = list(range(2015, settings.CURRENT_YEAR + 1))

    return render(request, 'filteredEmails.html', context)
