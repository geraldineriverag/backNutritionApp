from django.contrib import admin
from .models import Patient
from django.contrib.auth import get_user_model

# Importamos el modelo CustomUser para asociarlo con el paciente en el admin
User = get_user_model()

class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'nutritionist', 'height', 'current_weight', 'goal_type', 'work_activity', 'created_at', 'age'
    )  # Campos a mostrar en la lista de pacientes
    search_fields = ('user__email', 'user__first_name', 'user__last_name')  # Permite buscar por email y nombre
    list_filter = ('created_at', 'goal_type', 'work_activity', 'nutritionist')  # Filtros por fecha, meta de salud, actividad, nutricionista

    # Esto permite organizar los campos dentro de la vista de edición
    fieldsets = (
        (None, {
            'fields': ('user', 'nutritionist', 'height', 'current_weight', 'goal_type', 'work_activity', 'created_at')
        }),
        ('Salud y bienestar', {
            'fields': ('medical_condition', 'preexisting_condition', 'allergies', 'medications', 'digestive_issues', 'past_surgeries')
        }),
        ('Actividad física', {
            'fields': ('exercise_frequency', 'exercise_type', 'fitness_level')
        }),
        ('Hábitos alimenticios', {
            'fields': ('meals_per_day', 'meal_schedule', 'dietary_preferences', 'favorite_foods', 'avoided_foods', 'water_intake', 'alcohol_caffeine_consumption')
        }),
        ('Estilo de vida', {
            'fields': ('budget', 'cooking_time')
        }),
    )

    readonly_fields = ['created_at', 'age']  # No se puede modificar la fecha de creación ni la edad calculada

    def age(self, obj):
        """Retorna la edad calculada del paciente basada en su fecha de nacimiento"""
        return obj.age
    age.admin_order_field = 'user__birth_date'  # Permite ordenar por la fecha de nacimiento

# Registramos el modelo Patient en el admin
admin.site.register(Patient, PatientAdmin)


