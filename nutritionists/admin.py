from django.contrib import admin
from .models import Nutritionist

@admin.register(Nutritionist)
class NutritionistAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo Nutritionist."""
    list_display = (
        'user',
        'years_of_experience',
        'accepts_new_patients',
        'max_patients',
        'session_duration_minutes',
        'created_at',
    )
    search_fields = (
        'user__email',
        'education',
        'specialties',
        'languages',
    )
    list_filter = (
        'accepts_new_patients',
        'years_of_experience',
        'languages',
    )
    readonly_fields = (
        'created_at',
    )
    fieldsets = (
        (None, {
            'fields': ('user', 'profile_picture', 'bio')
        }),
        ('Formación y Especialidades', {
            'fields': ('education', 'specialties', 'languages', 'years_of_experience')
        }),
        ('Configuración', {
            'fields': ('accepts_new_patients', 'max_patients', 'session_duration_minutes', 'website')
        }),
        ('Tiempos', {
            'fields': ('created_at',)
        }),
    )
