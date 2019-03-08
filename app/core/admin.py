from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#helps to support multiple languages
from django.utils.translation import gettext as _

from core import models

#  change some class variables for support
#  Admin page stuff
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None,{'fields': ('email','password')} ),
        (_('Personal Info'), {'fields':('name',)}),
        (
            ('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        ( ('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets =(
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
