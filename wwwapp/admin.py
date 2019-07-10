from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Article, UserProfile, ArticleContentHistory, \
    WorkshopCategory, Workshop, WorkshopType, WorkshopParticipant, UserInfo, \
    WorkshopUserProfile

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


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

    def make_clear(self, _request, queryset):
        queryset.update(status=None)
    make_clear.short_description = "Zmień status na Null"

    actions = [make_acccepted, make_refused, make_clear]


admin.site.register(Workshop, WorkshopAdmin)

admin.site.register(UserInfo)

admin.site.register(Article)
admin.site.register(ArticleContentHistory)

admin.site.register(WorkshopCategory)
admin.site.register(WorkshopType)
admin.site.register(WorkshopParticipant)
admin.site.register(WorkshopUserProfile)
