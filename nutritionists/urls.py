from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NutritionistProfileView, NutritionistViewSet

router = DefaultRouter()
router.register(r'', NutritionistViewSet, basename='nutritionist')
urlpatterns = [
    path("me/", NutritionistProfileView.as_view(), name="nutritionist-profile"),
    path("", include(router.urls)),
]
