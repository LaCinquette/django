from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inlines(self, request, obj=None):
        if obj:
            return [ProfileInline]
        else:
            return []
    # list_display = ('email', 'username', 'first_name', 'last_name')
    # form = UserCreateForm2
    # add_form = UserCreateForm2
    # list_display = ('username', 'email', 'date_joined', 'last_login', 'is_staff', )
    # search_fields = ('email', )
    # readonly_fields = ('date_joined', 'last_login')
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    #     (_("Personal info"), {"fields": ("first_name", "last_name")}),
    #     (
    #         _("Permissions"),
    #         {
    #             "fields": (
    #                 "is_active",
    #                 "is_staff",
    #                 "is_superuser",
    #                 "company",
    #                 "groups",
    #                 "user_permissions",
    #             ),
    #         },
    #     ),
    #     (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    # )

    # add_fieldsets = (
    #         (
    #             None,
    #             {
    #                 'classes': ('wide',),
    #                 'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
    #             },
    #         ),
    # )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
