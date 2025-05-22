from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import CustomUser
from nutritionists.models import Nutritionist
from django.utils import timezone

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="patient_profile")
    nutritionist = models.ForeignKey(
        Nutritionist, on_delete=models.SET_NULL,
        related_name="patients", null=True, blank=True
    )

    height = models.FloatField(help_text="Altura en cm")
    current_weight = models.FloatField(help_text="Peso en kg")
    waist_circumference = models.FloatField(blank=True, null=True)
    hip_circumference = models.FloatField(blank=True, null=True)

    # Objetivos y salud
    goal_type = models.CharField(max_length=100, choices=[
        ("Pérdida de peso", "Pérdida de peso"),
        ("Ganar masa muscular", "Ganar masa muscular"),
        ("Mantenimiento", "Mantenimiento"),
        ("Mejorar hábitos", "Mejorar hábitos"),
        ("Tratar condición médica", "Tratar condición médica")
    ])
    medical_condition = models.CharField(max_length=255, blank=True, null=True)
    preexisting_condition = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    digestive_issues = models.TextField(blank=True, null=True)
    past_surgeries = models.TextField(blank=True, null=True)

    # Actividad física
    work_activity = models.CharField(max_length=50, choices=[
        ("Sedentario", "Sedentario"),
        ("Activo", "Activo"),
        ("Muy activo", "Muy activo")
    ])
    exercise_frequency = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(7)],
        help_text="Veces por semana"
    )
    exercise_type = models.CharField(max_length=255, blank=True, null=True)
    fitness_level = models.CharField(max_length=50, choices=[
        ("Bajo", "Bajo"),
        ("Moderado", "Moderado"),
        ("Alto", "Alto"),
    ])

    # Hábitos alimenticios
    meals_per_day = models.IntegerField()
    meal_schedule = models.TextField(blank=True, null=True)
    dietary_preferences = models.CharField(max_length=255, blank=True, null=True)
    favorite_foods = models.TextField(blank=True, null=True)
    avoided_foods = models.TextField(blank=True, null=True)
    water_intake = models.FloatField(help_text="Litros por día")
    alcohol_caffeine_consumption = models.TextField(blank=True, null=True)

    # Recursos y estilo de vida
    budget = models.FloatField(help_text="Presupuesto disponible para alimentación")
    cooking_time = models.CharField(max_length=50, choices=[
        ("Poco tiempo", "Poco tiempo"),
        ("Tiempo medio", "Tiempo medio"),
        ("Mucho tiempo", "Mucho tiempo"),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.email})"

    @property
    def age(self):
        """Calcula la edad en base al birth_date del usuario"""
        if self.user.birth_date:
            today = timezone.now().date()
            return today.year - self.user.birth_date.year - (
                (today.month, today.day) < (self.user.birth_date.month, self.user.birth_date.day)
            )
        return None
