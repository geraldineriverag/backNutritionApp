from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from nutritionists.models import Nutritionist
from patients.models import Patient


class Invitation(models.Model):
    """Modelo para gestionar las invitaciones enviadas por nutricionistas a pacientes."""

    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)  # Token único para cada invitación
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)

    # Valida que solo los nutricionistas con registro completo puedan invitar
    def clean(self):
        if not self.nutritionist.user.is_active:
            raise ValidationError('El nutricionista debe estar registrado completamente para enviar invitaciones.')
        super().clean()

    def accept(self, user):
        """
        Marca la invitación como aceptada y asocia/el paciente al nutricionista.
        """
        self.accepted    = True
        self.accepted_at = timezone.now()
        self.save()

        # Asocia perfil de paciente con este usuario
        # Si ya existe, actualiza sólo el nutritionist; si no, crea uno
        patient, created = Patient.objects.get_or_create(user=user)
        patient.nutritionist = self.nutritionist
        patient.save()
        return patient

    def __str__(self):
        return f"Invitación {self.token} → {self.email}"
