# nutritionists/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NutritionistProfileView, NutritionistViewSet

router = DefaultRouter()
router.register(r'', NutritionistViewSet, basename='nutritionist')  # Solo si vas a listar o usar admin

urlpatterns = [
    path("me/", NutritionistProfileView.as_view(), name="nutritionist-profile"),
    path("", include(router.urls)),
]
