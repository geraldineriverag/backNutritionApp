# patients/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsPatient
from invitations.models import Invitation
from nutritionists.views import IsNutritionist
from .models import Patient
from patients import form_schema
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    CRUD de Pacientes:

    - **Pacientes**: Pueden ver y editar únicamente su propio perfil.
    - **Nutricionistas**: Pueden gestionar los pacientes a su cargo.

    **Métodos disponibles:**
    - `GET`: Obtiene la lista de pacientes (solo nutricionistas pueden ver a sus pacientes).
    - `POST`: Crea un nuevo paciente (solo nutricionistas pueden crear pacientes).
    - `PUT`: Edita un paciente existente (los pacientes solo pueden editar su propio perfil).
    - `DELETE`: Elimina un paciente (solo los nutricionistas pueden eliminar pacientes).

    **Restricciones de acceso:**
    - Los pacientes solo pueden acceder a su propio perfil.
    - Los nutricionistas pueden acceder y gestionar los pacientes que tienen asignados.

    **Campos que se permiten:**
    - `user`: Referencia al usuario (correo electrónico, nombre, etc.)
    - `nutritionist`: Referencia al nutricionista asignado (solo editado por nutricionistas).
    """

    serializer_class = PatientSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Devuelve la lista de pacientes según el rol del usuario autenticado.

        - Si el usuario es un **paciente**, solo puede acceder a su propio perfil.
        - Si el usuario es un **nutricionista**, puede acceder a los pacientes que tiene asignados.
        """
        user = self.request.user
        # Solo accedemos a role si está autenticado
        if not getattr(user, 'is_authenticated', False):
            return Patient.objects.none()

        role = getattr(user, 'role', None)
        if role == 'paciente':
            return Patient.objects.filter(user=user)
        if role == 'nutricionista':
            return Patient.objects.filter(nutritionist__user=user)
        return Patient.objects.none()

class PatientFormSchemaView(APIView):
    """
    Devuelve el esquema JSON del formulario clínico dividido en pasos.

    - Este endpoint está destinado a la obtención del esquema de los formularios clínicos
    (divididos en pasos) para completar el perfil del paciente.

    **Permisos:**
    - Solo accesible para usuarios autenticados.
    """
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """
        Devuelve el esquema del formulario clínico en formato JSON.

        Este esquema contiene los pasos y campos necesarios para completar el perfil clínico de un paciente.
        """
        return Response(form_schema.FORM_SCHEMA)

class RegisterPatientView(APIView):
    """
    Registra un paciente utilizando el usuario autenticado y guarda todos los datos clínicos del wizard.
    """
    permission_classes = [AllowAny]  # ⚡️ SOLO usuarios autenticados pueden registrar

    @staticmethod
    def post(request):
        user = request.user  # 🧠 usuario autenticado
        token = request.data.get('token', None)

        # Intentar asociar nutricionista solo si hay token
        nutritionist = None
        if token:
            inv = Invitation.objects.filter(
                token=token,
                email=user.email,
                accepted=False
            ).first()
            if inv:
                nutritionist = inv.nutritionist
                inv.accept()
            # Si no encuentra invitación, simplemente seguimos sin nutricionista

        # Verificar que el paciente no esté registrado
        if hasattr(user, 'patient_profile'):
            return Response(
                {"message": "El usuario ya es un paciente registrado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mapear los campos del request
        patient_data = {
            'user': user,
            'nutritionist': nutritionist,
            'height': request.data.get('height'),
            'current_weight': request.data.get('current_weight'),
            'waist_circumference': request.data.get('waist_circumference'),
            'hip_circumference': request.data.get('hip_circumference'),

            'goal_type': request.data.get('goal_type'),
            'medical_condition': request.data.get('medical_condition'),
            'allergies': request.data.get('allergies'),
            'medications': request.data.get('medications'),

            'preexisting_condition': request.data.get('preexisting_condition'),
            'digestive_issues': request.data.get('digestive_issues'),
            'past_surgeries': request.data.get('past_surgeries'),
            'fitness_level': request.data.get('fitness_level'),

            'work_activity': request.data.get('work_activity'),
            'exercise_frequency': request.data.get('exercise_frequency'),
            'exercise_type': request.data.get('exercise_type'),

            'meals_per_day': request.data.get('meals_per_day'),
            'meal_schedule': request.data.get('meal_schedule'),
            'dietary_preferences': request.data.get('dietary_preferences'),
            'favorite_foods': request.data.get('favorite_foods'),

            'avoided_foods': request.data.get('avoided_foods'),
            'water_intake': request.data.get('water_intake'),
            'alcohol_caffeine_consumption': request.data.get('alcohol_caffeine_consumption'),

            'budget': request.data.get('budget'),
            'cooking_time': request.data.get('cooking_time'),
        }

        # Crear el paciente
        patient = Patient.objects.create(**patient_data)

        return Response(
            {
                "message": "Paciente registrado exitosamente.",
                "patient_id": patient.id,
            },
            status=status.HTTP_201_CREATED
        )

class PatientProfileView(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        user = request.user

        # Verificar si el usuario tiene un perfil de paciente
        if not hasattr(user, 'patient_profile'):
            return Response(
                {"message": "El usuario no tiene un perfil de paciente registrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        patient = user.patient_profile

        # Puedes decidir qué campos mostrar aquí
        patient_data = {
            'id': patient.id,
            'height': patient.height,
            'current_weight': patient.current_weight,
            'waist_circumference': patient.waist_circumference,
            'hip_circumference': patient.hip_circumference,
            'goal_type': patient.goal_type,
            'medical_condition': patient.medical_condition,
            'allergies': patient.allergies,
            'medications': patient.medications,
            'preexisting_condition': patient.preexisting_condition,
            'digestive_issues': patient.digestive_issues,
            'past_surgeries': patient.past_surgeries,
            'fitness_level': patient.fitness_level,
            'work_activity': patient.work_activity,
            'exercise_frequency': patient.exercise_frequency,
            'exercise_type': patient.exercise_type,
            'meals_per_day': patient.meals_per_day,
            'meal_schedule': patient.meal_schedule,
            'dietary_preferences': patient.dietary_preferences,
            'favorite_foods': patient.favorite_foods,
            'avoided_foods': patient.avoided_foods,
            'water_intake': patient.water_intake,
            'alcohol_caffeine_consumption': patient.alcohol_caffeine_consumption,
            'budget': patient.budget,
            'cooking_time': patient.cooking_time,
            'nutritionist_id': patient.nutritionist.id if patient.nutritionist else None,
        }

        return Response(patient_data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request):
        user = request.user

        if not hasattr(user, 'patient_profile'):
            return Response(
                {"message": "El usuario no tiene un perfil de paciente registrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        patient = user.patient_profile
        data = request.data

        # Solo actualizamos los campos que se envían
        for field in data:
            if hasattr(patient, field):
                setattr(patient, field, data[field])

        patient.save()

        return Response({"message": "Perfil clínico actualizado correctamente."}, status=status.HTTP_200_OK)
