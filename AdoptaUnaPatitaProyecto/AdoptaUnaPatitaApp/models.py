from django.db import models

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
    usuario = models.CharField(max_length=100)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    comentarios = models.TextField(blank=True)
    estado = models.CharField(max_length=50, default="Pendiente")

    def __str__(self):
        return f"Solicitud de {self.usuario} por {self.mascota.nombre}"


class Seguimiento(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return f"Seguimiento de {self.mascota.nombre}"
