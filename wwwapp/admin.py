from django.contrib import admin
from django.contrib.auth.models import User
from wwwapp.models import Article, UserProfile, ArticleContentHistory, WorkshopCategory, Workshop, WorkshopType
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)

admin.site.register(Article)
admin.site.register(ArticleContentHistory)

admin.site.register(WorkshopCategory)
admin.site.register(WorkshopType)
admin.site.register(Workshop)
