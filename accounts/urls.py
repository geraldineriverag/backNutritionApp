from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import RegisterUserView, CustomTokenObtainPairView, UserProfileView
from nutritionists.views import NutritionistViewSet

router = DefaultRouter()
router.register(r'nutritionists', NutritionistViewSet, basename='nutritionists')

urlpatterns = [
    # Registro
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

]
