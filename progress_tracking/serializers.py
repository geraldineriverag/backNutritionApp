from rest_framework import serializers
from .models import ProgressTracking


class ProgressTrackingSerializer(serializers.ModelSerializer):
    """
    Serializer para el seguimiento del progreso de los pacientes.

    **Campos:**
    - `id`: Identificador único del seguimiento (solo lectura).
    - `patient`: Paciente al que pertenece el seguimiento (relación con el modelo `Patient`).
    - `record_date`: Fecha en que se registró el seguimiento (solo lectura).
    - `weight`: Peso del paciente en ese seguimiento.
    - `waist_circumference`: Circunferencia de la cintura del paciente.
    - `hip_circumference`: Circunferencia de la cadera del paciente.
    - `bmi`: Índice de masa corporal calculado automáticamente en el modelo (solo lectura).
    - `body_fat_percentage`: Porcentaje de grasa corporal calculado automáticamente en el modelo (solo lectura).
    - `muscle_mass`: Masa muscular calculada automáticamente en el modelo (solo lectura).

    **Restricciones de acceso:**
    - Todos los campos son editables excepto `id`, `record_date`, `bmi`, `body_fat_percentage` y `muscle_mass` que son de solo lectura.

    **Métodos de validación y lógica:**
    - El cálculo del `bmi`, `body_fat_percentage` y `muscle_mass` se realiza automáticamente en el modelo cuando se guarda el registro.
    """

    class Meta:
        model = ProgressTracking
        fields = [
            'id',
            'patient',
            'record_date',
            'weight',
            'waist_circumference',
            'hip_circumference',
            'bmi',
            'body_fat_percentage',
            'muscle_mass',
        ]
        read_only_fields = ('id', 'record_date', 'bmi', 'body_fat_percentage', 'muscle_mass')

    def create(self, validated_data):
        """
        Crea un nuevo registro de seguimiento de progreso.

        El modelo `ProgressTracking` calcula automáticamente los valores de `bmi`,
        `body_fat_percentage` y `muscle_mass` cuando el registro se guarda.

        **Flujo**:
        - El serializer toma los datos validados y pasa la información al modelo.
        - El modelo calculará automáticamente los valores de `bmi`, `body_fat_percentage` y `muscle_mass`.

        :param validated_data: Los datos validados a partir de la solicitud.
        :return: Instancia del modelo `ProgressTracking` creada.
        """
        # En create() no hace falta nada especial porque el modelo calcula automáticamente.
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza un registro de seguimiento de progreso.

        Similar al método `create`, los cálculos de `bmi`, `body_fat_percentage` y
        `muscle_mass` se harán en el método `save()` del modelo, por lo que no es necesario
        realizar ninguna acción adicional aquí.

        **Flujo**:
        - El serializer valida los datos y luego los pasa al modelo para actualizar el registro.
        - El modelo actualizará automáticamente los valores de `bmi`, `body_fat_percentage` y `muscle_mass`.

        :param instance: Instancia del seguimiento a actualizar.
        :param validated_data: Los datos validados a partir de la solicitud.
        :return: Instancia del modelo `ProgressTracking` actualizada.
        """
        # En update() tampoco, los cálculos se harán en el save() del modelo.
        return super().update(instance, validated_data)
