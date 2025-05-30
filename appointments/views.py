from rest_framework import viewsets, permissions
from django.core.mail import send_mail
from .models import Appointment
from .serializers import AppointmentSerializer

class IsNutritionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'nutricionista'

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset         = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsNutritionist]

    def get_queryset(self):
        # Nutricionistas solo ven sus propias citas
        return Appointment.objects.filter(nutritionist=self.request.user.nutritionist_profile)

    def perform_create(self, serializer):
        # Asigna al nutricionista actual y guarda
        appt = serializer.save(nutritionist=self.request.user.nutritionist_profile)
        # Envío inmediato de confirmación
        send_mail(
            subject="Cita agendada",
            message=(
                f"Tienes una cita con "
                f"{appt.nutritionist.user.first_name} el "
                f"{appt.scheduled_for.strftime('%Y-%m-%d %H:%M')}."
            ),
            from_email="no-reply@tudominio.com",
            recipient_list=[appt.patient.user.email],
            fail_silently=True,
        )

