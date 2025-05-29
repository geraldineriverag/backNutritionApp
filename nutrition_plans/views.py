from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import NutritionPlan
from .serializers import NutritionPlanSerializer

class NutritionPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de planes nutricionales.

    Accesos:
    - Nutricionistas:
        - Pueden crear, listar, actualizar y eliminar planes nutricionales de sus pacientes.
    - Pacientes:
        - Solo pueden consultar (lectura) su propio plan nutricional.

    Endpoints:
    - CRUD completo sobre planes.
    - Acción adicional para obtener el PDF del plan.
    """
    serializer_class = NutritionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna el conjunto de planes nutricionales que puede ver el usuario autenticado.

        - Nutricionistas: sus propios planes asignados.
        - Pacientes: su propio plan.
        - Otros usuarios: no retornan nada.

        Returns:
            QuerySet: Planes filtrados según el rol del usuario.
        """
        user = self.request.user

        if not getattr(user, 'is_authenticated', False):
            return NutritionPlan.objects.none()

        role = getattr(user, 'role', None)
        if role == 'nutricionista':
            nutritionist_profile = getattr(user, 'nutritionist_profile', None)
            return NutritionPlan.objects.filter(nutritionist=nutritionist_profile)
        if role == 'paciente':
            return NutritionPlan.objects.filter(patient__user=user)

        return NutritionPlan.objects.none()

    @action(detail=True, methods=['get'])
    def get_pdf(self, request, *args, **kwargs):
        """
        Obtener la URL del archivo PDF del plan nutricional.

        Sólo accesible si el plan tiene un PDF asignado.

        Returns:
            Response: URL del PDF o mensaje de error si no existe.
        """
        plan = self.get_object()
        if plan.pdf_plan:
            return Response({'pdf_url': plan.pdf_plan.url})
        return Response(
            {'message': 'No hay archivo PDF disponible.'},
            status=status.HTTP_404_NOT_FOUND
        )

    def perform_create(self, serializer):
        """
        Asigna automáticamente el nutricionista autenticado al crear un plan.

        - Solo los usuarios con rol 'nutricionista' tendrán su perfil vinculado al nuevo plan.

        Args:
            serializer (NutritionPlanSerializer): Serializer con los datos validados.
        """
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == 'nutricionista':
            nutritionist_profile = getattr(user, 'nutritionist_profile', None)
            serializer.save(nutritionist=nutritionist_profile)
        else:
            serializer.save()

    def perform_update(self, serializer):
        """
        Asegura que al actualizar un plan se mantenga el nutricionista autenticado.

        Args:
            serializer (NutritionPlanSerializer): Serializer con los datos validados.
        """
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == 'nutricionista':
            nutritionist_profile = getattr(user, 'nutritionist_profile', None)
            serializer.save(nutritionist=nutritionist_profile)
        else:
            serializer.save()
