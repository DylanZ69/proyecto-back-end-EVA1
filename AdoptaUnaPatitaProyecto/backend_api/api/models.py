from django.db import models

class Refugio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    raza = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    # antes era FK -> ahora texto
    refugio_nombre = models.CharField(max_length=100)

class Solicitud(models.Model):
    nombre_adoptante = models.CharField(max_length=100)
    correo = models.EmailField()
    fecha = models.DateField(auto_now_add=True)

    # antes era FK -> ahora texto
    mascota_nombre = models.CharField(max_length=100)
