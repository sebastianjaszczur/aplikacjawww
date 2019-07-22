from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView

from wwwapp.settings import CURRENT_YEAR, DEBUG
from . import views, mail_views
from .auth import login_view, ScopedOAuthRedirect, ScopedOAuthCallback, \
    create_user_from_unmerged_access_view

urlpatterns = [
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('images/favicon.ico'),
            permanent=False),
        name="favicon"
    ),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login_view, name='login'),
    url(r'^accounts/login/(?P<provider>(\w|-)+)/$', ScopedOAuthRedirect.as_view(), name='scopedallaccess-login'),
    url(r'^accounts/callback/(?P<provider>(\w|-)+)/$', ScopedOAuthCallback.as_view(), name='scopedallaccess-callback'),
    url(r'^accounts/createUserFromAccess/$', create_user_from_unmerged_access_view, name='scopedallaccess-createUserFromAccess'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile_view, name='profile'),
    url(r'^profile/$', views.my_profile_view, name='myProfile'),
    url(r'^article/(?P<name>[a-zA-Z0-9\-_]+)/$', views.article_view, name='article'),
    url(r'^articleNameList/$', views.article_name_list_view, name='articleNameList'),
    url(r'^addArticle/$', views.article_view, name='addArticle'),
    url(r'^workshop/priv/(?P<name>[a-zA-Z0-9\-_]+)/$', views.workshop_view, name='workshop'),
    url(r'^workshop/(?P<name>[a-zA-Z0-9\-_]+)/$', views.workshop_page_view, name='workshop_page'),
    url(r'^workshop/participants/(?P<name>[a-zA-Z0-9\-_]+)/$', views.workshop_participants_view, name='workshop_participants'),
    url(r'^savePoints/$', views.save_points_view),
    url(r'^register/$', views.register_to_workshop_view, name='register_to_workshop'),
    url(r'^unregister/$', views.unregister_from_workshop_view, name='unregister_from_workshop'),
    url(r'^qualProblems/(?P<workshop_name>[a-zA-Z0-9\-_]+)/$', views.qualification_problems_view, name='qualification_problems'),
    url(r'^addWorkshop/$', views.workshop_view, name='addWorkshop'),
    url(r'^yourWorkshops/$', views.your_workshops_view, name='yourWorkshops'),
    url(r'^allWorkshops/$', views.all_workshops_view, name='allWorkshops'),
    url(r'^dataForPlan/$', views.data_for_plan_view, name='dataForPlan'),
    url(r'^participants/$', RedirectView.as_view(url='/%d/participants/' % CURRENT_YEAR, permanent=False), name='participants'),
    url(r'^([0-9]+)/participants/$', views.participants_view, name='year_participants'),
    url(r'^lecturers/$', RedirectView.as_view(url='/%d/lecturers/' % CURRENT_YEAR, permanent=False), name='lecturers'),
    url(r'^([0-9]+)/lecturers/$', views.lecturers_view, name='year_lecturers'),
    url(r'^emails/$', views.emails_view, name='emails'),
    url(r'^filterEmails/(?:(?P<year>[0-9]+)/(?P<filter_id>[a-zA-Z0-9\-_]+)/)?$', mail_views.filtered_emails_view, name='filter_emails'),
    url(r'^template_for_workshop_page/$', views.template_for_workshop_page_view, name='template_for_workshop_page'),
    url(r'^program/$', RedirectView.as_view(url='/%d/program/' % CURRENT_YEAR, permanent=False), name='program'),
    url(r'^([0-9]+)/program/$', views.program_view, name='year_program'),
    url(r'^robots\.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^$', views.index_view, name='index'),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
