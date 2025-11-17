from django import forms
from .models import Mascota, Refugio, Solicitud, Usuario

class MascotaForm(forms.ModelForm):

    class Meta:
        model = Mascota
        fields = ['nombre', 'edad', 'raza', 'tipo','refugio']

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        edad = cleaned_data.get('edad')
        raza = cleaned_data.get('raza') 
        tipo = cleaned_data.get('tipo')

        if nombre and any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener números")

        if edad <1 or edad > 25:
            raise forms.ValidationError("La edad debe estar entre 1 y 25")
        
        if raza and any(char.isdigit() for char in raza):
            raise forms.ValidationError("La raza no puede contener números")

        if tipo and any(char.isdigit() for char in tipo):
            raise forms.ValidationError("El tipo no puede contener números")
        return cleaned_data
    
class RefugioForm(forms.ModelForm):

    class Meta:
        model = Refugio
        fields = ['nombre', 'direccion', 'telefono']

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        telefono = cleaned_data.get('telefono')

        if nombre and any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener números")
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo puede contener números")

        return cleaned_data

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'nombre_adoptante',
            'correo_adoptante',
            'mascota_fk',
        ]

        widgets = {
            'mascota_fk': forms.Select(),
        }

    def clean_nombre_adoptante(self):
        nombre = self.cleaned_data.get('nombre_adoptante')
        if any(c.isdigit() for c in nombre):
            raise forms.ValidationError("El nombre no puede contener números.")
        return nombre


    
class SolicitudPublicForm(forms.Form):
    nombre_adoptante = forms.CharField(max_length=100)
    correo_adoptante = forms.EmailField()
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.all())


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


   
   