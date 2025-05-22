from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, PatientProfileView, PatientFormSchemaView, RegisterPatientView

router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patients')

urlpatterns = [
    path("me/", PatientProfileView.as_view(), name="patient-profile"),
    path("form-schema/", PatientFormSchemaView.as_view(), name="patient-form-schema"),
    path("register/", RegisterPatientView.as_view(), name="register-patient"),
    path("", include(router.urls)),
]
