from django.db import models
from patients.models import Patient

class ProgressTracking(models.Model):
    """Historial de progreso de un paciente."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="progress_records")
    record_date = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(blank=True, null=True)
    waist_circumference = models.FloatField(blank=True, null=True)
    hip_circumference = models.FloatField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    body_fat_percentage = models.FloatField(blank=True, null=True)
    muscle_mass = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["-record_date"]

    def __str__(self):
        return f"{self.patient.user.first_name} - {self.record_date.strftime('%Y-%m-%d')}"

    def calculate_bmi(self):
        """Calcula el IMC automáticamente."""
        if self.patient.height and self.weight:
            height_in_meters = self.patient.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None

    def calculate_body_fat_percentage(self):
        """Calcula el porcentaje de grasa corporal."""
        if self.weight and self.waist_circumference and self.patient.height:
            age = self.patient.age if self.patient.age else 0
            bmi = self.calculate_bmi()
            return round((1.2 * bmi) + (0.23 * age) - 5.4, 2)
        return None

    def calculate_muscle_mass(self):
        """Calcula la masa muscular estimada."""
        if self.weight and self.body_fat_percentage:
            return round(self.weight * (1 - (self.body_fat_percentage / 100)), 2)
        return None

    def save(self, *args, **kwargs):
        self.bmi = self.calculate_bmi()
        self.body_fat_percentage = self.calculate_body_fat_percentage()
        self.muscle_mass = self.calculate_muscle_mass()
        super().save(*args, **kwargs)
