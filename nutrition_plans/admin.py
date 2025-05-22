# nutrition_plan/admin.py

from django.contrib import admin
from .models import NutritionPlan

@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para NutritionPlan."""

    list_display = (
        'patient',
        'nutritionist',
        'calories',
        'caloric_needs',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'patient__user__email',
        'patient__user__first_name',
        'patient__user__last_name',
        'nutritionist__user__email',
        'nutritionist__user__first_name',
        'nutritionist__user__last_name',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'nutritionist',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (None, {
            'fields': ('patient', 'nutritionist')
        }),
        ('Plan de comidas', {
            'fields': ('meal_plan', 'pdf_plan', 'review_date'),
            'description': 'Descripción general del plan, archivo PDF (opcional) y fecha de revisión.'
        }),
        ('Macronutrientes', {
            'fields': ('calories', 'caloric_needs', 'protein', 'carbs', 'fats'),
        }),
        ('Tiempos', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
