from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RefugioViewSet, MascotaViewSet, SolicitudViewSet

router = DefaultRouter()
router.register(r"refugios", RefugioViewSet)
router.register(r"mascotas", MascotaViewSet)
router.register(r"solicitudes", SolicitudViewSet)

urlpatterns = [
  path("", include(router.urls)),
]
