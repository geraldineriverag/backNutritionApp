# progress_tracking/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProgressTrackingViewSet

router = DefaultRouter()
router.register(r'', ProgressTrackingViewSet, basename='progress')

urlpatterns = [
    # Todas las rutas CRUD quedan mapeadas aquí:
    # GET    /           → list()
    # POST   /           → create()
    # GET    /{pk}/      → retrieve()
    # PUT    /{pk}/      → update()
    # PATCH  /{pk}/      → partial_update()
    # DELETE /{pk}/      → destroy()
    path('', include(router.urls)),
]
