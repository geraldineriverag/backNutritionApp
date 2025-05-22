from django.contrib import admin
from progress_tracking.models import ProgressTracking


class ProgressTrackingAdmin(admin.ModelAdmin):
    list_display = ("patient", "record_date", "weight", "bmi", "body_fat_percentage", "muscle_mass")
    search_fields = ("patient__user__first_name", "record_date")
    list_filter = ("record_date",)
    ordering = ("-record_date",)

admin.site.register(ProgressTracking, ProgressTrackingAdmin)
