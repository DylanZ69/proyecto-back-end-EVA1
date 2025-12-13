from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rol")
    search_fields = ("user__username", "rol")
    list_filter = ("rol",)
