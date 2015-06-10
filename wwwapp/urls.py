from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from wwwapp import views
from wwwapp import mail_views
from wwwapp import settings
from wwwapp.auth import loginView, ScopedOAuthRedirect, ScopedOAuthCallback, createUserFromUnmergedAccess

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wwwapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('images/favicon.ico'),
            permanent=False),
        name="favicon"
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', loginView, name='login'),
    url(r'^accounts/login/(?P<provider>(\w|-)+)/$', ScopedOAuthRedirect.as_view(), name='scopedallaccess-login'),
    url(r'^accounts/callback/(?P<provider>(\w|-)+)/$', ScopedOAuthCallback.as_view(), name='scopedallaccess-callback'),
    url(r'^accounts/createUserFromAccess/$', createUserFromUnmergedAccess, name='scopedallaccess-createUserFromAccess'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^updateProfilePage/$', views.update_profile_page, name='update_profile_page'),
    url(r'^updateCoverLetter/$', views.update_cover_letter, name='update_cover_letter'),
    url(r'^profile/$', views.my_profile, name='myProfile'),
    url(r'^article/(?P<name>[a-zA-Z0-9\-_]+)/$', views.article, name='article'),
    url(r'^articleNameList/$', views.article_name_list, name='articleNameList'),
    url(r'^addArticle/$', views.article, name='addArticle'),
    url(r'^workshop/priv/(?P<name>[a-zA-Z0-9\-_]+)/$', views.workshop, name='workshop'),
    url(r'^workshop/(?P<name>[a-zA-Z0-9\-_]+)/$', views.workshop_page, name='workshop_page'),
    url(r'^workshop/participants/(?P<name>[a-zA-Z0-9\-_]+)/$', views.workshop_participants, name='workshop_participants'),
    url(r'^register/$', views.register_to_workshop, name='register_to_workshop'),
    url(r'^unregsiter/$', views.unregister_from_workshop, name='unregister_from_workshop'),
    url(r'^qualProblems/(?P<workshop_name>[a-zA-Z0-9\-_]+)/$', views.qualification_problems, name='qualification_problems'),
    url(r'^addWorkshop/$', views.workshop, name='addWorkshop'),
    url(r'^yourWorkshops/$', views.your_workshops, name='yourWorkshops'),
    url(r'^allWorkshops/$', views.all_workshops, name='allWorkshops'),
    url(r'^participants/$', views.participants, name='participants'),
    url(r'^emails/$', views.emails, name='emails'),
    url(r'^filterEmails/(?:(?P<filter_id>[a-zA-Z0-9\-_]+)/)?$', mail_views.filtered_emails, name='filter_emails'),
    url(r'^template_for_workshop_page/$', views.template_for_workshop_page, name='template_for_workshop_page'),
    url(r'^program/$', views.program, name='program'),
    url(r'^$', views.index, name='index'),
)
