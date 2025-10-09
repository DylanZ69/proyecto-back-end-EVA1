from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------
    # RUTAS HTML
    # ----------------------------
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('menu/', views.menu, name='menu'),
    # ----------------------------
    # MASCOTAS
    # ----------------------------
    path('mascotas/', views.ver_mascotas, name='listar_mascotas'),
    path('mascotas/<int:id>/', views.obtener_mascota, name='obtener_mascota'),
    path('mascotas/crear/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/actualizar/<int:id>/', views.actualizar_mascota, name='actualizar_mascota'),
    path('mascotas/eliminar/<int:id>/', views.eliminar_mascota, name='eliminar_mascota'),

    # ----------------------------
    # REFUGIOS
    # ----------------------------
    path('refugios/', views.ver_refugios, name='ver_refugios'),
    path('refugios/', views.listar_refugios, name='listar_refugios'),
    path('refugios/crear/', views.crear_refugio, name='crear_refugio'),
    path('refugios/actualizar/<int:id>/', views.actualizar_refugio, name='actualizar_refugio'),
    path('refugios/eliminar/<int:id>/', views.eliminar_refugio, name='eliminar_refugio'),

    # ----------------------------
    # SOLICITUDES DE ADOPCIÓN
    # ----------------------------
    # urls.py
    
    path('solicitudes/', views.ver_solicitudes, name='ver_solicitudes'),
    path('enviar_solicitud/', views.enviar_solicitud, name='enviar_solicitud'),
    path('solicitudes/nueva/', views.enviar_solicitud, name='enviar_solicitud'),
    path('solicitudes/', views.ver_solicitudes, name='ver_solicitudes'),
    path('solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('solicitudes/crear/', views.crear_solicitud, name='crear_solicitud'),
    path('solicitudes/actualizar/<int:id>/', views.actualizar_solicitud, name='actualizar_solicitud'),
    path('solicitudes/eliminar/<int:id>/', views.eliminar_solicitud, name='eliminar_solicitud'),

    # ----------------------------
    # SEGUIMIENTOS
    # ----------------------------
    path('seguimientos/', views.listar_seguimientos, name='listar_seguimientos'),
    path('seguimientos/crear/', views.crear_seguimiento, name='crear_seguimiento'),
    path('seguimientos/actualizar/<int:id>/', views.actualizar_seguimiento, name='actualizar_seguimiento'),
    path('seguimientos/eliminar/<int:id>/', views.eliminar_seguimiento, name='eliminar_seguimiento'),
]
