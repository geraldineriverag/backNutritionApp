from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    # Campos “bonus” que sacan el nombre completo del paciente
    patient_name = serializers.CharField(source='patient.user.first_name', read_only=True)
    patient_last_name = serializers.CharField(source='patient.user.last_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'patient_name',
            'patient_last_name',
            'scheduled_for',
            'created_at',
        ]
        read_only_fields = ['id']
