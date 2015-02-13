from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from wwwapp.models import Article, ArticleForm

def get_context(request):
    context = {}
    
    articles_on_menubar = Article.objects.filter(on_menubar=True).all()
    context['articles_on_menubar'] = articles_on_menubar
    
    return context

def login(request):
    context = get_context(request)
    if request.user.is_authenticated():
        try:
            access = request.user.accountaccess_set.all()[0]
        except IndexError:
            access = None
        else:
            client = access.api_client
            context['info'] = client.get_profile_info(raw_token=access.access_token)
    return render(request, 'login.html', context)


def article(request, name):
    context = get_context(request)
    art = Article.objects.get(name=name)
    
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=art)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('article', args=(form.instance.name,)))
        else:
            form = ArticleForm(instance=art)
    else:
        form = None
    
    context['article'] = art
    context['form'] = form

    return render(request, 'article.html', context)


def as_article(name):
    # make sure that article with this name exists
    art = Article.objects.get_or_create(name=name)
    
    def page(request):
        return article(request, name)
    return page


index = as_article("index")
