from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("", views.login_view, name="login"),
    path("menu/", views.menu, name="menu"),
    path("logout/", views.logout_view, name="logout"),

    # --------------------
    # MASCOTAS (CRUD)
    # --------------------
    path("mascotas/", views.ver_mascotas, name="ver_mascotas"),
    path("mascotas/crear/", views.crear_mascota, name="crear_mascota"),
    path("mascotas/<int:id>/editar/", views.actualizar_mascota, name="actualizar_mascota"),
    path("mascotas/<int:id>/eliminar/", views.eliminar_mascota, name="eliminar_mascota"),

    # --------------------
    # REFUGIOS (CRUD)
    # --------------------
    path("refugios/", views.ver_refugios, name="ver_refugios"),
    path("refugios/crear/", views.crear_refugio, name="crear_refugio"),
    path("refugios/<int:id>/editar/", views.actualizar_refugio, name="actualizar_refugio"),
    path("refugios/<int:id>/eliminar/", views.eliminar_refugio, name="eliminar_refugio"),

    # --------------------
    # SOLICITUDES (CRUD)
    # --------------------
    path("solicitudes/", views.ver_solicitudes, name="ver_solicitudes"),
    path("solicitudes/crear/", views.crear_solicitud, name="crear_solicitud"),
    path("solicitudes/<int:id>/editar/", views.actualizar_solicitud, name="actualizar_solicitud"),
    path("solicitudes/<int:id>/eliminar/", views.eliminar_solicitud, name="eliminar_solicitud"),
]
