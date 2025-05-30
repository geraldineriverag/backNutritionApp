from django.db import models
from django.utils import timezone
from patients.models import Patient
from nutritionists.models import Nutritionist

class Appointment(models.Model):
    patient       = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    nutritionist  = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name="appointments")
    scheduled_for = models.DateTimeField(help_text="Fecha y hora de la cita")
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita {self.patient.user.email} ↔ {self.nutritionist.user.email} @ {self.scheduled_for}"
