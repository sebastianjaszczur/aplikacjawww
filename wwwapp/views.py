# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib import messages
from django.contrib.auth.models import User
from wwwapp.models import Article, UserProfile, Workshop, WorkshopParticipant
from wwwapp.forms import ArticleForm, UserProfileForm, UserForm, WorkshopForm, UserProfilePageForm, \
    WorkshopPageForm, UserCoverLetterForm
from wwwapp.templatetags.wwwtags import qualified_mark

def get_context(request):
    context = {}

    articles_on_menubar = Article.objects.filter(on_menubar=True).all()
    if not request.user.is_authenticated():
        has_workshops = False
    else:
        if Workshop.objects.filter(lecturer__user=request.user).exists():
            has_workshops = True
        else:
            has_workshops = False

    context['google_analytics_key'] = settings.GOOGLE_ANALYTICS_KEY
    context['articles_on_menubar'] = articles_on_menubar
    context['has_workshops'] = has_workshops

    return context


def program(request):
    context = get_context(request)
    context['title'] = 'Program WWW11'

    if request.user.is_authenticated():
        user_participation = set(Workshop.objects.filter(participants__user=request.user).all())
    else:
        user_participation = set()

    workshops = Workshop.objects.filter(status='Z').order_by('title').prefetch_related('lecturer', 'lecturer__user', 'category')
    context['workshops'] = [(workshop, (workshop in user_participation)) for workshop
                            in workshops ]

    if request.user.is_authenticated():
        qualifications = WorkshopParticipant.objects.filter(participant__user=request.user).prefetch_related('workshop')
        if not any(qualification.qualification_result is not None for qualification in qualifications):
            qualifications = None
        context['your_qualifications'] = qualifications

    return render(request, 'program.html', context)


def profile(request, user_id):
    """
    This function allows to view other people's profile by id.
    However, to view them easily some kind of resolver might be needed as we don't have usernames.
    """
    context = get_context(request)
    user_id = int(user_id)
    user = get_object_or_404(User, pk=user_id)

    profile = UserProfile.objects.get(user=user)
    profile_page = profile.profile_page

    is_my_profile = (request.user == user)
    can_see_all_users = request.user.has_perm('wwwapp.see_all_users')

    context['title'] = u"{0.first_name} {0.last_name}".format(user)
    context['profile_page'] = profile_page
    context['is_my_profile'] = is_my_profile

    if can_see_all_users or is_my_profile:
        context['profile'] = profile

    return render(request, 'profile.html', context)


def redirect_after_profile_save(request, target):
    messages.info(request, u'Zapisano.')
    return redirect(reverse('myProfile') + '#' + target)

def update_profile_page(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        user_profile = UserProfile.objects.get(user=request.user)

        if request.method == "POST":
            user_profile_page_form = UserProfilePageForm(request.POST, instance=user_profile)
            if user_profile_page_form.is_valid():
                user_profile_page_form.save()

        return redirect_after_profile_save(request, 'profile_page')

def update_cover_letter(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        user_profile = UserProfile.objects.get(user=request.user)

        if request.method == "POST":
            user_cover_letter_form = UserCoverLetterForm(request.POST, instance=user_profile)
            if user_cover_letter_form.is_valid():
                user_cover_letter_form.save()

        return redirect_after_profile_save(request, 'cover_letter')


def my_profile(request):
    context = get_context(request)
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == "POST":
            user_form = UserForm(request.POST, instance=request.user)
            user_profile_form = UserProfileForm(request.POST, instance=user_profile)
            if user_form.is_valid() and user_profile_form.is_valid():
                user_form.save()
                user_profile_form.save()

            return redirect_after_profile_save(request, 'data')
        else:
            user_form = UserForm(instance=request.user)
            user_profile_form = UserProfileForm(instance=user_profile)
            user_form.helper.form_tag = False
            user_profile_form.helper.form_tag = False
            context['user_form'] = user_form
            context['user_profile_form'] = user_profile_form
            context['user_profile_page_form'] = UserProfilePageForm(instance=user_profile)
            context['user_cover_letter_form'] = UserCoverLetterForm(instance=user_profile)
            context['is_editing_profile'] = True
            context['title'] = u'Mój profil'

            return render(request, 'profile.html', context)


def workshop(request, name=None):
    context = get_context(request)
    new = (name is None)
    if new:
        workshop = None
        title = u'Nowe warsztaty'
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            has_perm_to_edit = True
    else:
        workshop = Workshop.objects.get(name=name)
        title = workshop.title
        if request.user.is_authenticated():
            has_perm_to_edit = Workshop.objects.filter(name=name, lecturer__user=request.user).exists()
        else:
            has_perm_to_edit = False

    if has_perm_to_edit:
        if request.method == 'POST':
            form = WorkshopForm(request.POST, instance=workshop)
            if form.is_valid():
                workshop = form.save(commit=False)
                workshop.save()
                form.save_m2m()
                user_profile = UserProfile.objects.get(user=request.user)
                workshop.lecturer.add(user_profile)
                workshop.save()
                return redirect('workshop', form.instance.name)
        else:
            form = WorkshopForm(instance=workshop)
    else:
        form = None

    context['addWorkshop'] = new
    context['title'] = title
    context['workshop'] = workshop
    context['form'] = form
    context['has_perm_to_edit'] = has_perm_to_edit

    return render(request, 'workshop.html', context)


def workshop_page(request, name):
    context = get_context(request)

    workshop = get_object_or_404(Workshop, name=name)
    if workshop.status != 'Z': # Zaakceptowane
        raise Http404("Warsztaty nie zostały zaakceptowane")

    title = workshop.title
    has_perm_to_edit = can_edit_workshop(workshop, request.user)

    if has_perm_to_edit:
        if request.method == 'POST':
            form = WorkshopPageForm(request.POST, request.FILES, instance=workshop)
            if form.is_valid():
                workshop = form.save(commit=False)
                workshop.save()
                form.save_m2m()
                user_profile = UserProfile.objects.get(user=request.user)
                workshop.lecturer.add(user_profile)
                workshop.save()
                return redirect('workshop_page', form.instance.name)
        else:
            if not workshop.page_content:
                workshop_template = Article.objects.get(name="template_for_workshop_page").content
                workshop.page_content = workshop_template
                workshop.save()
            form = WorkshopPageForm(instance=workshop)
    else:
        form = None

    context['title'] = title
    context['workshop'] = workshop
    context['form'] = form
    context['has_perm_to_edit'] = has_perm_to_edit

    return render(request, 'workshoppage.html', context)

def can_edit_workshop(workshop, user):
    if user.is_authenticated():
        return Workshop.objects.filter(id=workshop.id, lecturer__user=user).exists()
    else:
        return False

def workshop_participants(request, name):
    workshop = get_object_or_404(Workshop, name=name)

    can_see_all = request.user.has_perm('wwwapp.see_all_workshops')
    can_see_this = can_edit_workshop(workshop, request.user)

    if not can_see_all and not can_see_this:
        # it should show page like "you don't have permission", probably
        return redirect('login')

    context = get_context(request)

    context['title'] = workshop.title
    context['workshop_participants'] = WorkshopParticipant.objects.filter(workshop=workshop).prefetch_related(
        'workshop', 'participant', 'participant__user')

    return render(request, 'workshopparticipants.html', context)

def save_points(request):
    workshop_participant = WorkshopParticipant.objects.get(id=request.POST['id'])
    # can edit?
    can_edit = can_edit_workshop(workshop_participant.workshop, request.user)
    if not can_edit:
        return JsonResponse({'error': u'Brak uprawnień.'})

    try:
        result = request.POST['points'].strip()
        if result == '':
            result = None
        workshop_participant.qualification_result = result
    except (ValidationError, ValueError):
        return JsonResponse({'error': u'Niepoprawny format liczby'})

    workshop_participant.save()
    workshop_participant = WorkshopParticipant.objects.get(id=workshop_participant.id)

    return JsonResponse({'value': str(workshop_participant.qualification_result),
                         'mark': qualified_mark(workshop_participant.is_qualified())})

def participants(request):
    can_see_users = request.user.has_perm('wwwapp.see_all_workshops')

    if not can_see_users:
        return redirect('login')

    participants = WorkshopParticipant.objects.all().prefetch_related('workshop', 'participant', 'participant__user')

    people = {}

    for participant in participants:
        p_id = participant.participant.id
        if p_id not in people:
            cover_letter = participant.participant.cover_letter
            people[p_id] = {
                'user': participant.participant.user,
                'accepted_workshop_count': 0,
                'workshop_count': 0,
                'has_letter': bool(cover_letter and len(cover_letter) > 50)
            }

        people[p_id]['workshop_count'] += 1
        if participant.is_qualified():
            people[p_id]['accepted_workshop_count'] += 1

    people = people.values()
    people.sort(key=lambda p: (-p['has_letter'], -p['accepted_workshop_count']))

    context = get_context(request)
    context['title'] = 'Uczestnicy'
    context['people'] = people

    return render(request, 'participants.html', context)


def register_to_workshop(request):
    workshop_name = request.POST['workshop_name']

    if not request.user.is_authenticated():
        return JsonResponse({'redirect': reverse('login')})

    workshop = get_object_or_404(Workshop, name=workshop_name)

    if workshop.qualification_threshold is not None:
        return JsonResponse({'error': u'Kwalifikacja na te warsztaty została zakończona.'})

    WorkshopParticipant(participant=UserProfile.objects.get(user=request.user), workshop=workshop).save()

    context = get_context(request)
    context['workshop'] = workshop
    context['registered'] = True
    return JsonResponse({'content': render_to_response('_programworkshop.html', context).content})

def unregister_from_workshop(request):
    workshop_name = request.POST['workshop_name']
    data = {}
    if not request.user.is_authenticated():
        data['redirect'] = reverse('login')
        return JsonResponse(data)

    workshop = get_object_or_404(Workshop, name=workshop_name)
    profile = UserProfile.objects.get(user=request.user)
    workshop_participant = WorkshopParticipant.objects.get(workshop=workshop, participant=profile)

    if workshop.qualification_threshold is not None or workshop_participant.qualification_result is not None:
        return JsonResponse({'error': u'Kwalifikacja na te warsztaty została zakończona - nie możesz się wycofać.'})

    workshop_participant.delete()

    context = get_context(request)
    context['workshop'] = workshop
    context['registered'] = False
    data['content'] = render_to_response('_programworkshop.html', context).content
    return JsonResponse(data)


def qualification_problems(request, workshop_name):
    workshop = get_object_or_404(Workshop, name=workshop_name)
    filename = workshop.qualification_problems.path

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Length'] = os.path.getsize(filename)
    return response


def article(request, name = None):
    context = get_context(request)
    new = (name is None)
    if new:
        art = None
        title = u'Nowy artykuł'
        has_perm = request.user.has_perm('wwwapp.add_article')
    else:
        art = Article.objects.get(name=name)
        title = art.title
        has_perm = request.user.has_perm('wwwapp.change_article')

    if has_perm:
        if request.method == 'POST':
            form = ArticleForm(request.user, request.POST, instance=art)
            if form.is_valid():
                article = form.save(commit=False)
                article.modified_by = request.user
                article.save()
                form.save_m2m()
                return redirect('article', form.instance.name)
        else:
            form = ArticleForm(request.user, instance=art)
    else:
        form = None

    context['addArticle'] = new
    context['title'] = title
    context['article'] = art
    context['form'] = form

    return render(request, 'article.html', context)


def article_name_list(request):
    names = Article.objects.values_list('name', flat=True)
    return JsonResponse(list(names), safe=False)


def your_workshops(request):
    if not request.user.is_authenticated():
        return redirect('login')
    context = get_context(request)

    workshops = Workshop.objects.filter(lecturer__user=request.user)
    context['workshops'] = workshops
    context['title'] = u'Twoje warsztaty'

    return render(request, 'workshoplist.html', context)


def all_workshops(request):
    if not request.user.has_perm('wwwapp.see_all_workshops'):
        # it should show page like "you don't have permission", probably
        return redirect('login')
    context = get_context(request)

    workshops = Workshop.objects.all()
    context['workshops'] = workshops
    context['title'] = u'Wszystkie warsztaty'

    return render(request, 'workshoplist.html', context)


def emails(request):
    # think about seperate permission
    if not request.user.has_perm('wwwapp.see_all_workshops'):
        # it should show page like "you don't have permission", probably
        return redirect('login')

    workshops = Workshop.objects.all()

    result = []
    for workshop in workshops:
        lecturer = workshop.lecturer.all()[0]
        email = lecturer.user.email
        name = lecturer.user.first_name + " " + lecturer.user.last_name

        to_append = {'workshopname': workshop.title, 'email': email, 'name': name}
        result.append(to_append)

    return JsonResponse(result, safe=False)

def as_article(name):
    # make sure that article with this name exists
    art = Article.objects.get_or_create(name=name)

    def page(request):
        return article(request, name)
    return page

index = as_article("index")
template_for_workshop_page = as_article("template_for_workshop_page")
