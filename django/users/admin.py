from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    min_num = 1
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inlines(self, request, obj=None):
        if obj:
            return [ProfileInline]
        else:
            return []
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
