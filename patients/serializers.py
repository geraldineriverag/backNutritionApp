from rest_framework import serializers
from accounts.serializers import UserRegistrationSerializer
from nutritionists.models import Nutritionist
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer para la gestión de pacientes. Este serializer se utiliza para:

    - Visualizar los datos del paciente.
    - Modificar los datos de los pacientes por parte de nutricionistas.
    - Asignar un nutricionista a un paciente (solo nutricionistas pueden hacerlo).
    - Calcular la edad del paciente de manera automática.

    **Campos:**
    - `user`: Información del usuario asociada al paciente.
    - `nutritionist`: Nutricionista asignado al paciente (solo modificable por nutricionistas).
    - `age`: Edad calculada automáticamente (solo lectura).
    """

    user = UserRegistrationSerializer(read_only=True)
    nutritionist = serializers.PrimaryKeyRelatedField(
        queryset=Nutritionist.objects.all(),
        allow_null=True,
        required=False
    )
    age = serializers.ReadOnlyField()  # Edad calculada

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_at', 'age']  # ya no incluimos 'bmi'

    def validate(self, data):
        """
        Validación adicional antes de guardar los datos del paciente.

        - Los nutricionistas pueden asignar o cambiar el nutricionista del paciente.
        - Si un nutricionista crea un paciente sin especificar un nutricionista,
          se asigna el nutricionista autenticado como el encargado del paciente.

        **Condiciones de validación:**
        - Si el usuario no es un nutricionista, no puede asignar un nutricionista.
        - Si un nutricionista crea un paciente y no se especifica un nutricionista,
          se asigna automáticamente al nutricionista autenticado.
        """

        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            # Solo los nutricionistas pueden asignar/modificar nutricionista en el paciente
            if not user.is_nutritionist and 'nutritionist' in data:
                raise serializers.ValidationError(
                    "Solo los nutricionistas pueden asignar o cambiar nutricionista."
                )
            # Si un nutricionista crea el paciente sin haber pasado un nutritionist explícito
            if request.method == 'POST' and user.is_nutritionist and not data.get('nutritionist'):
                data['nutritionist'] = user.nutritionist_profile

        return data
