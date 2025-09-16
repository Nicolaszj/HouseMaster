from django.contrib.auth.models import User
from django.db import models
from core.models import Compra as CoreCompra  # si 7


class Propiedad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Compra(models.Model):
    propiedad = models.ForeignKey('propiedades.Propiedad', on_delete=models.CASCADE, related_name='compras_propiedades')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras_propiedades')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} compró {self.propiedad.titulo}"
