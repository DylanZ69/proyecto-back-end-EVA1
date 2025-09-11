from django.contrib import admin
from django.urls import path, include
# Importa el panel de administración de Django y funciones para definir rutas y enlazar apps

urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),

    # Incluye todas las URLs definidas en la app "AdoptaUnaPatitaApp"
    # Esto permite que las rutas de la app se carguen automáticamente
    path('', include("AdoptaUnaPatitaApp.urls")),
]
