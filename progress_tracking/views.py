from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.exceptions import PermissionDenied

from .models import ProgressTracking
from .serializers import ProgressTrackingSerializer
from accounts.models import CustomUser
from django.utils.dateparse import parse_date

class ProgressTrackingViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los registros de progreso de los pacientes.

    Permite a los pacientes ver y crear su propio progreso, y a los nutricionistas ver el progreso de sus pacientes.
    Soporta filtrado por fechas mediante los parámetros de consulta `start_date` y `end_date`.
    """
    queryset = ProgressTracking.objects.all().order_by('-record_date')
    serializer_class = ProgressTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Obtener registros de progreso",
        description=(
            "Devuelve una lista de registros de progreso. "
            "Los pacientes solo ven su propio seguimiento, mientras que los nutricionistas pueden ver los seguimientos de sus pacientes."
        ),
        parameters=[
            OpenApiParameter(
                name="start_date",
                description="Fecha inicial para filtrar registros (YYYY-MM-DD)",
                required=False,
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name="end_date",
                description="Fecha final para filtrar registros (YYYY-MM-DD)",
                required=False,
                type=OpenApiTypes.DATE,
            ),
        ],
        responses={200: ProgressTrackingSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        # Partimos del queryset base
        qs = ProgressTracking.objects.all().order_by('-record_date')

        # Filtramos según el rol
        if isinstance(user, CustomUser):
            if hasattr(user, 'patient_profile') and user.role == 'paciente':
                qs = qs.filter(patient=user.patient_profile)
            elif user.role == 'nutricionista':
                qs = qs.filter(patient__nutritionist__user=user)

        # Filtrado adicional por fechas de consulta
        params = getattr(self.request, 'query_params', self.request.GET)
        start_date = params.get('start_date')
        end_date = params.get('end_date')

        if start_date:
            dt = parse_date(start_date)
            if dt:
                qs = qs.filter(record_date__date__gte=dt)

        if end_date:
            dt = parse_date(end_date)
            if dt:
                qs = qs.filter(record_date__date__lte=dt)

        return qs

    @extend_schema(
        summary="Crear un registro de progreso",
        description=(
            "Crea un nuevo registro de progreso para el paciente autenticado. "
            "Solo los pacientes pueden crear sus propios registros, que luego serán calculados automáticamente en el modelo."
        ),
        responses={201: ProgressTrackingSerializer}
    )
    def perform_create(self, serializer):
        user = self.request.user

        # Verifica que el usuario sea un paciente
        if isinstance(user, CustomUser) and hasattr(user, 'patient_profile') and user.role == 'paciente':
            patient = user.patient_profile
        else:
            raise PermissionDenied("Solo los pacientes pueden registrar progresos.")

        # Asignar al paciente automáticamente y guardar el progreso
        serializer.save(patient=patient)



