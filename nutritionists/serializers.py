from rest_framework import serializers
from .models import Nutritionist
from accounts.serializers import UserRegistrationSerializer  # Asumiendo que ya lo tienes

class NutritionistSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Nutritionist (lectura general).

    - Incluye la información del usuario asociado (serializada de forma de solo lectura).
    - Todos los campos del modelo son expuestos.
    """

    user = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = Nutritionist
        fields = '__all__'
        read_only_fields = ['created_at']


class NutritionistUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar información de un Nutritionist.

    - Excluye el campo 'user' y 'created_at' ya que no deben ser modificables.
    - Utilizado en endpoints donde el nutricionista puede actualizar su perfil profesional.
    """

    class Meta:
        model = Nutritionist
        exclude = ['user', 'created_at']
