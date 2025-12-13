from rest_framework import serializers
from .models import Refugio, Mascota, Solicitud

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = "__all__"

    def validate_edad(self, value):
        if value < 0 or value > 40:
            raise serializers.ValidationError("Edad inválida.")
        return value

class RefugioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refugio
        fields = "__all__"

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = "__all__"

    def validate_correo(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Correo inválido.")
        return value
