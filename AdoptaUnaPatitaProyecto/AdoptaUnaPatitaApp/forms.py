from django import forms
from .models import Mascota, Refugio, Solicitud, Usuario

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
        fields = ['nombre_adoptante','correo_adoptante', 'mascota_id','mascota_nombre', 'comentarios']

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,  # Oculta la contraseña en el input
        min_length=4,
        required=True
    )

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'rol']  # Campos que quieres mostrar en el form
        widgets = {
            'rol': forms.Select(choices=[('usuario', 'Usuario'), ('admin', 'Administrador')])
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("El usuario ya existe")
        return username