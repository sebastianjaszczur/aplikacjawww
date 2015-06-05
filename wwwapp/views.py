#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
import os
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.models import User
from wwwapp.models import Article, UserProfile, Workshop
from wwwapp.forms import ArticleForm, UserProfileForm, UserForm, WorkshopForm, UserProfilePageForm, \
                         WorkshopPageForm


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


def program(request):  #  Not so sure about 'program' - maybe 'agenda' is better
    context = get_context(request)
    context['title'] = 'Program WWW11'
    
    if request.user.is_authenticated():
        user_participation = set(Workshop.objects.filter(participants__user=request.user).all())
    else:
        user_participation = set()
    context['workshops'] = [(workshop, (workshop in user_participation)) for workshop
                            in Workshop.objects.filter(status='Z').order_by('title')]
    
    return render(request, 'program.html', context)


def set_form_readonly(form):
    for field in form:
        form.fields[field.name].widget.attrs['disabled'] = 'True'
    return form


def profile(request, user_id):  # Can't get printing gender right :(
    """
    This function allows to view other people's profile by id.
    However, to view them easily some kind of resolver might be needed as we don't have usernames.
    """
    # we don't want to make users' emails public - so we have to check for permission to view
    if not request.user.has_perm('wwwapp.see_all_users'):
        # it should show page like "you don't have permission", probably
        return redirect('login')
    
    context = get_context(request)
    user_id = int(user_id)
    user = get_object_or_404(User, pk=user_id)
    if request.user == user:
        return redirect('myProfile')
    profile_page = UserProfile.objects.get(user=user).profile_page

    context['title'] = u"{0.first_name} {0.last_name}".format(user)
    context['profile_page'] = profile_page
    context['myProfile'] = False

    return render(request, 'profile.html', context)


def update_profile_page(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == "POST":
            user_profile_page_form = UserProfilePageForm(request.POST, instance=user_profile)
            if user_profile_page_form.is_valid():
                user_profile_page_form.save()
            return redirect('myProfile')
        else:
            return redirect('myProfile')


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
            return redirect('myProfile')
        else:
            user_form = set_form_readonly(UserForm(instance=request.user))
            user_profile_form = set_form_readonly(UserProfileForm(instance=user_profile))
            user_form.helper.form_tag = False
            user_profile_form.helper.form_tag = False
            context['user_form'] = user_form
            context['user_profile_form'] = user_profile_form
            context['user_profile_page_form'] = UserProfilePageForm(instance=user_profile)
            context['myProfile'] = True
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
    if request.user.is_authenticated():
        has_perm_to_edit = Workshop.objects.filter(name=name, lecturer__user=request.user).exists()
    else:
        has_perm_to_edit = False
    
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

def register_to_workshop(request):
    workshop_name = request.POST['workshop_name']
    data = {}
    if not request.user.is_authenticated():
        data['redirect'] = reverse('login')
        return JsonResponse(data)
    workshop = get_object_or_404(Workshop, name=workshop_name)
    workshop.participants.add(UserProfile.objects.get(user=request.user))
    workshop.save()
    context = get_context(request)
    context['workshop'] = workshop
    context['registered'] = True
    data['content'] = render_to_response('_programworkshop.html', context).content
    return JsonResponse(data)

def unregister_from_workshop(request):
    workshop_name = request.POST['workshop_name']
    data = {}
    if not request.user.is_authenticated():
        data['redirect'] = reverse('login')
        return JsonResponse(data)
    workshop = get_object_or_404(Workshop, name=workshop_name)
    workshop.participants.remove(UserProfile.objects.get(user=request.user))
    workshop.save()
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
