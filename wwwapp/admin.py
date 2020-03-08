from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Article, UserProfile, ArticleContentHistory, \
    WorkshopCategory, Workshop, WorkshopType, WorkshopParticipant, UserInfo, \
    WorkshopUserProfile, ResourceYearPermission

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    readonly_fields = ['userinfo_link', ]

    def userinfo_link(self, instance):
        # TODO: Render it as an inline instead - I just can't get it to work with a nested relation like that...
        if instance.id:
            userinfo_url = reverse('admin:wwwapp_userinfo_change', args=(instance.id,))
            return u'<a href="%s">UserInfo details</a>' % userinfo_url
        return u''
    userinfo_link.allow_tags = True
    userinfo_link.short_description = ''


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


admin.site.register(User, UserProfileAdmin)


class WorkshopAdmin(admin.ModelAdmin):
    def make_acccepted(self, _request, queryset):
        queryset.update(status='Z')
    make_acccepted.short_description = "Zmień status na Zaakceptowane"

    def make_refused(self, _request, queryset):
        queryset.update(status='O')
    make_refused.short_description = "Zmień status na Odrzucone"

    def make_cancelled(self, _request, queryset):
        queryset.update(status='X')
    make_cancelled.short_description = "Zmień status na Odwołane"

    def make_clear(self, _request, queryset):
        queryset.update(status=None)
    make_clear.short_description = "Zmień status na Null"

    actions = [make_acccepted, make_refused, make_cancelled, make_clear]


admin.site.register(Workshop, WorkshopAdmin)

admin.site.register(UserInfo)

admin.site.register(Article)
admin.site.register(ArticleContentHistory)

admin.site.register(WorkshopCategory)
admin.site.register(WorkshopType)
admin.site.register(WorkshopParticipant)
admin.site.register(WorkshopUserProfile)

admin.site.register(ResourceYearPermission)
