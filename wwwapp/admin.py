#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from wwwapp.models import Article, UserProfile, ArticleContentHistory, WorkshopCategory, Workshop, WorkshopType
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

class WorkshopAdmin(admin.ModelAdmin):
    def make_acccepted(modeladmin, request, queryset):
        queryset.update(status='Z')
    make_acccepted.short_description = "Zmień status na Zaakceptowane"
    def make_refused(modeladmin, request, queryset):
        queryset.update(status='O')
    make_refused.short_description = "Zmień status na Odrzucone"
    def make_clear(modeladmin, request, queryset):
        queryset.update(status=None)
    make_clear.short_description = "Zmień status na Null"
    
    actions = [make_acccepted, make_refused, make_clear]

admin.site.register(User, UserProfileAdmin)

admin.site.register(Article)
admin.site.register(ArticleContentHistory)

admin.site.register(WorkshopCategory)
admin.site.register(WorkshopType)
admin.site.register(Workshop, WorkshopAdmin)
