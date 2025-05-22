from django.db import models
from accounts.models import CustomUser

class Nutritionist(models.Model):
    """Perfil extendido para nutricionistas."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="nutritionist_profile")

    # Información profesional
    bio = models.TextField(blank=True, null=True, help_text="Breve biografía o descripción del nutricionista")
    education = models.CharField(max_length=255, blank=True, null=True, help_text="Formación académica")
    specialties = models.CharField(max_length=255, blank=True, null=True, help_text="Áreas de especialización")
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True, help_text="Idiomas hablados")

    # Configuraciones personalizadas
    accepts_new_patients = models.BooleanField(default=True)
    max_patients = models.PositiveIntegerField(default=50, help_text="Máximo de pacientes activos permitidos")
    session_duration_minutes = models.PositiveIntegerField(default=30)

    # Otros
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name
