from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from accounts.views import CustomTokenObtainPairView

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OpenAPI schema and documentation UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Account registration and user management
    path('api/accounts/', include('accounts.urls')),

    # Nutritionist endpoints (profile and management)
    path('api/nutritionists/', include('nutritionists.urls')),

    # Patient registration and form schema
    path('api/patients/', include('patients.urls')),

    # Nutrition plans management
    path('api/plan/', include('nutrition_plans.urls')),

    # Invitation management
    path('api/invitations/', include('invitations.urls')),

    # Progress tracking endpoints
    path('api/progress/', include('progress_tracking.urls')),
]
