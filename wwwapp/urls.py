from django.conf.urls import patterns, include, url
from django.contrib import admin
from wwwapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wwwapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/(?P<provider>(\w|-)+)/$', views.ScopedOAuthRedirect.as_view(), name='scopedallaccess-login'),    
    url(r'^profile/', views.profile, name='profile'),
    url(r'^article/(?P<name>[a-zA-Z0-9\-_]+)/', views.article, name='article'),
    url(r'^articleNameList/', views.article_name_list, name='articleNameList'),
    url(r'^addArticle/', views.article, name='addArticle'),
    url(r'^workshop/(?P<name>[a-zA-Z0-9\-_]+)/', views.workshop, name='workshop'),
    url(r'^addWorkshop/', views.workshop, name='addWorkshop'),
    url(r'^yourWorkshops/', views.your_workshops, name='yourWorkshops'),
    url(r'^$', views.index, name='index'),
)
