from django.urls import path
from . import views
# Importa path para definir URLs y views para asociar cada ruta con su función correspondiente

urlpatterns = [
    # ===========================
    # Páginas principales
    # ===========================
    path('', views.index, name="index"),            # Página de inicio
    path('login/', views.login_view, name="login"), # Página de login
    path('menu/', views.menu, name="menu"),         # Menú principal según rol

    # ===========================
    # Rutas de mascotas
    # ===========================
    path('mascotas/', views.mascotas, name="mascotas"),                  # Lista de mascotas
    path('mascotas/agregar/', views.agregar_mascota, name="agregar_mascota"), # Agregar nueva mascota (solo admin)
    path('mascotas/eliminar/<int:id>/', views.eliminar_mascota, name="eliminar_mascota"), # Eliminar mascota por ID (solo admin)

    # ===========================
    # Rutas de refugios
    # ===========================
    path('refugios/', views.refugios, name="refugios"),                   # Lista de refugios
    path('refugios/agregar/', views.agregar_refugio, name="agregar_refugio"), # Agregar refugio (solo admin)

    # ===========================
    # Rutas de solicitudes de adopción
    # ===========================
    path('solicitudes/', views.solicitudes, name="solicitudes"),                           # Lista de solicitudes
    path('solicitudes/enviar/', views.enviar_solicitud, name="enviar_solicitud"),         # Enviar nueva solicitud (solo usuario)
    path('solicitudes/gestionar/<int:id>/<str:accion>/', views.gestionar_solicitud, name="gestionar_solicitud"), # Aceptar o rechazar solicitud (solo admin)

    # ===========================
    # Rutas de seguimientos
    # ===========================
    path("seguimientos/", views.seguimientos, name="seguimientos"), # Lista de seguimientos (solo admin)
]
