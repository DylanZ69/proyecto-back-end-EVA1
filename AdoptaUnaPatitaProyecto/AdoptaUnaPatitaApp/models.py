from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
# ========================
# MODELOS PRINCIPALES
# ========================

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    raza = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Refugio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre



class Solicitud(models.Model):
    nombre_adoptante = models.CharField(max_length=100)
    correo_adoptante = models.EmailField()
    mascota_id = models.IntegerField(null=True, blank=True)  # Reemplaza FK
    mascota_nombre = models.CharField(max_length=100, blank=True)  # Guarda nombre de la mascota
    comentarios = models.TextField(blank=True)
    estado = models.CharField(max_length=20, default="Pendiente")
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_adoptante} - {self.mascota_nombre}"

class Seguimiento(models.Model):
    mascota_id = models.IntegerField(default=0)  # Reemplaza FK
    mascota_nombre = models.CharField(max_length=100)  # Para mostrar en vistas
    usuario = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return f"Seguimiento de {self.mascota_nombre}"
    

class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # se guarda hash
    rol = models.CharField(max_length=10, choices=[('admin','Admin'),('usuario','Usuario')])

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
