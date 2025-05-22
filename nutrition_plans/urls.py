# nutrition_plan/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import NutritionPlanViewSet

router = DefaultRouter()
# Registramos el ViewSet bajo el prefijo 'planes-nutricionales'
router.register(r'', NutritionPlanViewSet, basename='nutritionplan')

urlpatterns = [
    path('', include(router.urls)),
]
