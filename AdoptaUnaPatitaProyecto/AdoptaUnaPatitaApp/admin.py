from django.contrib import admin
from .models import Mascota, Refugio, Solicitud, Seguimiento

# Registra los modelos para que aparezcan en el panel admin
admin.site.register(Mascota)
admin.site.register(Refugio)
admin.site.register(Solicitud)
admin.site.register(Seguimiento)
