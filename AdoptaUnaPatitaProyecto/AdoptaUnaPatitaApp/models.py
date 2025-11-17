from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# ========================
# MODELOS PRINCIPALES
# ========================

class Refugio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    raza = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    #  CLAVE FORÁNEA AGREGADA 
    refugio = models.ForeignKey(Refugio, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.nombre


class Solicitud(models.Model):
    nombre_adoptante = models.CharField(max_length=100)
    correo_adoptante = models.EmailField()

    # FK real
    mascota_fk = models.ForeignKey(Mascota, null=True, blank=True, on_delete=models.SET_NULL)

    # Campos auxiliares (para mostrar rápido en tablas)
    mascota_id = models.IntegerField(null=True, blank=True)
    mascota_nombre = models.CharField(max_length=100, blank=True)

    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_adoptante} - {self.mascota_nombre}"



class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    rol = models.CharField(max_length=10, choices=[('admin','Admin'),('usuario','Usuario')])

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
