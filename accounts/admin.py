from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    ordering = ('email',)
    search_fields = ('username', 'email', 'first_name', 'last_name')  # <-- Incluido username

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  # <-- Incluido username
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'phone', 'birth_date', 'role')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'role', 'password1', 'password2'),  # <-- Incluido username
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

