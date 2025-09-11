from django.urls import path
from . import views

urlpatterns = [
  
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('menu/', views.menu, name="menu"),

  
    path('mascotas/', views.mascotas, name="mascotas"),
    path('mascotas/agregar/', views.agregar_mascota, name="agregar_mascota"),
    path('mascotas/eliminar/<int:id>/', views.eliminar_mascota, name="eliminar_mascota"),

  
    path('refugios/', views.refugios, name="refugios"),
    path('refugios/agregar/', views.agregar_refugio, name="agregar_refugio"),

  
    path('solicitudes/', views.solicitudes, name="solicitudes"),
    path('solicitudes/enviar/', views.enviar_solicitud, name="enviar_solicitud"),
    path('solicitudes/gestionar/<int:id>/<str:accion>/', views.gestionar_solicitud, name="gestionar_solicitud"),

    path("seguimientos/", views.seguimientos, name="seguimientos"),
]
