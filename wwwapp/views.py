#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from wwwapp.models import Article, UserProfile, Workshop
from wwwapp.forms import ArticleForm, UserProfileForm, UserForm, WorkshopForm

def get_context(request):
    context = {}
    
    articles_on_menubar = Article.objects.filter(on_menubar=True).all()
    context['articles_on_menubar'] = articles_on_menubar
    
    return context

def profile(request):
    context = get_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == "POST":
            user_form = UserForm(request.POST, instance=request.user)
            user_profile_form = UserProfileForm(request.POST, instance=user_profile)
            if user_form.is_valid() and user_profile_form.is_valid():
                user_form.save()
                user_profile_form.save()
        else:
            user_form = UserForm(instance=request.user)
            user_profile_form = UserProfileForm(instance=user_profile)
        context['user_form'] = user_form
        context['user_profile_form'] = user_profile_form
        return render(request, 'profile.html', context)

def login(request):
    context = get_context(request)
    if request.user.is_authenticated():
        try:
            access = request.user.accountaccess_set.all()[0]
        except IndexError:
            access = None
        else:
            client = access.api_client
            user_info = client.get_profile_info(raw_token=access.access_token)        
            context['info'] = user_info
            
            user = request.user
            user_profile, just_created = UserProfile.objects.get_or_create(user=user)
            
            if just_created:
                if 'first_name' in user_info:
                    user.first_name = user_info['first_name']
                if 'last_name' in user_info:
                    user.last_name = user_info['last_name']
                if 'gender' in user_info:
                    user_profile.gender = user_info['gender']
                user.save()
                user_profile.save()
    return render(request, 'login.html', context)


def workshop(request, name=None):
    context = get_context(request)
    new = (name is None)
    if new:
        workshop = None
        title = u'Nowe warsztaty'
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        else:
            has_perm = True
    else:
        workshop = Workshop.objects.get(name=name)
        title = workshop.title
        has_perm = Workshop.objects.filter(lecturer__user=request.user).exists()
    
    if has_perm:
        if request.method == 'POST':
            form = WorkshopForm(request.POST, instance=workshop)
            if form.is_valid():
                workshop = form.save(commit=False)
                workshop.save()
                user_profile = UserProfile.objects.get(user=request.user)
                workshop.lecturer.add(user_profile)
                workshop.save()
                return HttpResponseRedirect(reverse('workshop', args=(form.instance.name,)))
        else:
            form = WorkshopForm(instance=workshop)
    else:
        form = None
    
    context['addWorkshop'] = new
    context['title'] = title
    context['workshop'] = workshop
    context['form'] = form
    context['has_perm'] = has_perm

    return render(request, 'workshop.html', context)


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
                return HttpResponseRedirect(reverse('article', args=(form.instance.name,)))
        else:
            form = ArticleForm(request.user, instance=art)
    else:
        form = None
    
    context['addArticle'] = new
    context['title'] = title
    context['article'] = art
    context['form'] = form

    return render(request, 'article.html', context)


def your_workshops(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    context = get_context(request)
    
    workshops = Workshop.objects.filter(lecturer__user=request.user)
    context['workshops'] = workshops
    context['canAddWorkshop'] = True
    context['listTitle'] = "Twoje warsztaty"
    
    return render(request, 'workshoplist.html', context)


def as_article(name):
    # make sure that article with this name exists
    art = Article.objects.get_or_create(name=name)
    
    def page(request):
        return article(request, name)
    return page


index = as_article("index")
