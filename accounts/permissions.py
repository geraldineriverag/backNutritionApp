# permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsNutritionistOrReadOnly(BasePermission):
    """
    Permite solo a los nutricionistas modificar los datos.
    Los pacientes pueden leer sus propios datos, y los nutricionistas también.
    """

    def has_object_permission(self, request, view, obj):
        # Permitir lectura (GET, HEAD, OPTIONS) si el usuario es dueño del recurso
        if request.method in SAFE_METHODS:
            # Caso 1: El objeto tiene un campo 'user' (como CustomUser)
            if hasattr(obj, "user") and obj.user == request.user:
                return True
            # Caso 2: El objeto pertenece a un paciente y es su perfil
            if hasattr(obj, "patient") and obj.patient.user == request.user:
                return True
            # Caso 3: El objeto pertenece a un nutricionista
            if hasattr(obj, "nutritionist") and obj.nutritionist.user == request.user:
                return True
            return False

        # Permitir modificación solo si el usuario es el nutricionista asignado
        if hasattr(obj, "nutritionist") and obj.nutritionist.user == request.user:
            return True

        return False


class IsPatient(BasePermission):
    """
    Permite acceso solo a usuarios autenticados con rol 'paciente'.
    Útil para vistas generales de pacientes.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "paciente"


class IsConfirmedPatient(BasePermission):
    """
    Permite acceso solo a pacientes con un nutricionista asignado.
    Útil para vistas que requieren relación establecida con un nutricionista.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and getattr(request.user, "role", None) == "paciente":
            patient = getattr(request.user, 'patient_profile', None)
            return patient and patient.nutritionist is not None
        return False
