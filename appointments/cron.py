from django.utils import timezone
from django.core.mail import send_mail
from .models import Appointment
from datetime import timedelta

def send_reminders():
    morning = (timezone.now() + timedelta(days=1)).date()
    citas = Appointment.objects.filter(scheduled_for__date=morning)
    for c in citas:
        send_mail(
            subject="Recordatorio de cita",
            message=(
                f"Recuerda tu cita con "
                f"{c.nutritionist.user.first_name} mañana a las "
                f"{c.scheduled_for.strftime('%H:%M')}."
            ),
            from_email="no-reply@tudominio.com",
            recipient_list=[c.patient.user.email],
            fail_silently=True,
        )
