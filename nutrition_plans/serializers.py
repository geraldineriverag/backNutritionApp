from rest_framework import serializers
from django.utils import timezone
from .models import NutritionPlan

class NutritionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer para la representación y validación de planes nutricionales.

    Este serializer gestiona:
    - Creación de planes nutricionales.
    - Validación de datos ingresados.
    - Actualización controlada de campos específicos.
    """

    class Meta:
        model = NutritionPlan
        fields = [
            'id',
            'patient',
            'nutritionist',
            'created_at',
            'updated_at',
            'meal_plan',
            'calories',
            'caloric_needs',
            'protein',
            'carbs',
            'fats',
            'pdf_plan',
            'review_date'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validaciones adicionales antes de crear o actualizar un plan.

        - Impide que un paciente tenga más de un plan nutricional activo (solo al crear).
        - Verifica que la fecha de revisión no sea anterior a la fecha de creación real.
        """
        # 1️⃣ Evitamos que un paciente ya existente tenga otro plan al CREAR
        if self.instance is None and NutritionPlan.objects.filter(patient=data.get('patient')).exists():
            raise serializers.ValidationError("Este paciente ya tiene un plan nutricional asignado.")

        # 2️⃣ Validamos review_date contra la fecha de creación
        review_date = data.get('review_date')
        if review_date:
            # Si estamos EDITANDO, usamos la fecha real de creación; si no, comparamos contra ahora
            created_at = self.instance.created_at if self.instance else timezone.now()
            if review_date < created_at:
                raise serializers.ValidationError(
                    "La fecha de revisión no puede ser anterior a la fecha de creación del plan."
                )

        return data

    def create(self, validated_data):
        """
        Crea un nuevo plan, asignando automáticamente el nutricionista
        autenticado (si existe).
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['nutritionist'] = request.user.nutritionist_profile
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza campos específicos de un plan existente.
        """
        instance.meal_plan            = validated_data.get('meal_plan', instance.meal_plan)
        instance.calories             = validated_data.get('calories', instance.calories)
        instance.caloric_needs        = validated_data.get('caloric_needs', instance.caloric_needs)
        instance.protein              = validated_data.get('protein', instance.protein)
        instance.carbs                = validated_data.get('carbs', instance.carbs)
        instance.fats                 = validated_data.get('fats', instance.fats)
        instance.pdf_plan             = validated_data.get('pdf_plan', instance.pdf_plan)
        instance.review_date          = validated_data.get('review_date', instance.review_date)
        instance.save()
        return instance
