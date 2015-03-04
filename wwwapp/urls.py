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
    url(r'^login/', views.login, name='login'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^article/(?P<name>[a-zA-Z0-9\-_]+)/', views.article, name='article'),
    url(r'^$', views.index, name='index'),
)
