from django.db import models
from nutritionists.models import Nutritionist
from patients.models import Patient

class NutritionPlan(models.Model):
    """Plan nutricional de un paciente."""
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="nutrition_plan")
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name="nutrition_plans")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meal_plan = models.TextField(help_text="Descripción general del plan de comidas.")
    calories = models.PositiveIntegerField(help_text="Total de calorías diarias recomendadas.")
    caloric_needs = models.IntegerField(help_text="Necesidades calóricas basales del paciente.")
    protein = models.FloatField(null=True, blank=True, help_text="Cantidad recomendada de proteínas (gramos).")
    carbs = models.FloatField(null=True, blank=True, help_text="Cantidad recomendada de carbohidratos (gramos).")
    fats = models.FloatField(null=True, blank=True, help_text="Cantidad recomendada de grasas (gramos).")
    pdf_plan = models.FileField(upload_to='nutrition_plans/', null=True, blank=True, help_text="Subir el plan nutricional completo en formato PDF.")
    review_date = models.DateTimeField(null=True, blank=True, help_text="Fecha de revisión del plan nutricional.")  # Nueva fecha de revisión

    def __str__(self):
        return f"Plan nutricional de {self.patient.user.first_name} ({self.patient.user.email})"

    class Meta:
        verbose_name = "Plan nutricional"
        verbose_name_plural = "Planes nutricionales"
