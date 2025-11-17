from django.urls import path
from . import views

urlpatterns = [

    # ==============================
    # AUTENTICACIÓN
    # ==============================
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('menu/', views.menu, name='menu'),


    # ==============================
    # CRUD MASCOTAS
    # ==============================
    path('mascotas/', views.ver_mascotas, name='listar_mascotas'),
    path('mascotas/<int:id>/', views.obtener_mascota, name='obtener_mascota'),

    path('mascotas/crear/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/actualizar/<int:id>/', views.actualizar_mascota, name='actualizar_mascota'),
    path('mascotas/eliminar/<int:id>/', views.eliminar_mascota, name='eliminar_mascota'),


    # ----------------------------
    # REFUGIOS
    # ----------------------------
    path('refugios/', views.ver_refugios, name='ver_refugios'),
    path('refugios/listar/', views.listar_refugios, name='listar_refugios'),  # API JSON
    path('refugios/crear/', views.crear_refugio, name='crear_refugio'),
    path('refugios/actualizar/<int:id>/', views.actualizar_refugio, name='actualizar_refugio'),
    path('refugios/eliminar/<int:id>/', views.eliminar_refugio, name='eliminar_refugio'),
    path('refugios/<int:id>/', views.detalle_refugio, name='detalle_refugio'),



  # ==============================
    # CRUD SOLICITUDES
    # ==============================

    path('solicitudes/', views.ver_solicitudes, name='ver_solicitudes'),
    path('solicitudes/enviar/', views.enviar_solicitud, name='enviar_solicitud'),
    path('solicitudes/<int:id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('solicitudes/actualizar/<int:id>/', views.actualizar_solicitud, name='actualizar_solicitud'),
    path('solicitudes/eliminar/<int:id>/', views.eliminar_solicitud, name='eliminar_solicitud'),



    
]
