from django.contrib import admin
from .models import Mascota, Refugio, Solicitud, Usuario


# -------------------------
# ADMIN MASCOTA
# -------------------------
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "edad", "raza", "tipo", "refugio")
    search_fields = ("nombre", "raza", "tipo")
    list_filter = ("tipo", "refugio")
    ordering = ("nombre",)


# -------------------------
# ADMIN REFUGIO
# -------------------------
@admin.register(Refugio)
class RefugioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "direccion", "telefono")
    search_fields = ("nombre", "direccion")
    ordering = ("nombre",)


# -------------------------
# ADMIN SOLICITUD (Sin comentarios ni estado)
# -------------------------
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre_adoptante",
        "correo_adoptante",
        "mascota_fk",
        "fecha",
    )
    search_fields = ("nombre_adoptante", "correo_adoptante", "mascota_nombre")
    list_filter = ("fecha",)
    readonly_fields = ("fecha", "mascota_id", "mascota_nombre")

    fieldsets = (
        ("Datos del adoptante", {
            "fields": ("nombre_adoptante", "correo_adoptante")
        }),
        ("Mascota seleccionada", {
            "fields": ("mascota_fk", "mascota_id", "mascota_nombre")
        }),
    )


# -------------------------
# ADMIN USUARIO
# -------------------------
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "rol")
    search_fields = ("username",)
    list_filter = ("rol",)
