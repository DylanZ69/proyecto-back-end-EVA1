from django import forms
from .models import Mascota, Refugio, Solicitud

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'edad', 'raza', 'tipo']

class RefugioForm(forms.ModelForm):
    class Meta:
        model = Refugio
        fields = ['nombre', 'direccion', 'telefono']

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['usuario', 'mascota', 'comentarios']
