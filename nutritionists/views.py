from rest_framework import viewsets, permissions, status, generics
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Nutritionist
from .serializers import (
    NutritionistSerializer,
    NutritionistUpdateSerializer,
)

class IsNutritionist(permissions.BasePermission):
    """
    Permite acceso solo a usuarios autenticados con role='nutricionista'.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'nutricionista'
        )

class NutritionistProfileView(generics.RetrieveUpdateAPIView):
    """
    GET    /api/nutritionists/me/   → Recupera el perfil (200 o 404)
    POST   /api/nutritionists/me/   → Crea perfil parcial (201)
    PATCH  /api/nutritionists/me/   → Actualiza campos parciales (200)
    """
    serializer_class = NutritionistSerializer
    permission_classes = [IsNutritionist]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self):
        user = self.request.user
        if not hasattr(user, 'nutritionist_profile'):
            raise NotFound(detail="No profile")
        return user.nutritionist_profile  # type: ignore

    def get_serializer_class(self):
        # para POST/PATCH usamos el serializer de actualización parcial
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return NutritionistUpdateSerializer
        return NutritionistSerializer

    def post(self, request, *args, **kwargs):
        # creación parcial
        if hasattr(request.user, 'nutritionist_profile'):
            return Response(
                {"detail": "Ya existe perfil"},
                status=status.HTTP_400_BAD_REQUEST
            )
        ser = self.get_serializer(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        profile = ser.save(user=request.user)
        out = NutritionistSerializer(profile)
        return Response(out.data, status=status.HTTP_201_CREATED)


class NutritionistViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para perfiles de nutricionistas.
    - Solo para usuarios autenticados con role='nutricionista'.
    """
    queryset = Nutritionist.objects.all()
    serializer_class = NutritionistSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NutritionistUpdateSerializer
        return NutritionistSerializer
