from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Refugio, Mascota, Solicitud
from .serializers import RefugioSerializer, MascotaSerializer, SolicitudSerializer

class RefugioViewSet(viewsets.ModelViewSet):
    queryset = Refugio.objects.all()
    serializer_class = RefugioSerializer
    permission_classes = [IsAuthenticated]

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
    permission_classes = [IsAuthenticated]

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated]
