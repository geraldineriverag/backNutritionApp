from django.contrib import admin
from .models import Invitation

class InvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "nutritionist", "token", "accepted", "created_at")
    search_fields = ("email", "nutritionist__user__first_name")
    list_filter = ("accepted",)
    ordering = ("-created_at",)

admin.site.register(Invitation, InvitationAdmin)

