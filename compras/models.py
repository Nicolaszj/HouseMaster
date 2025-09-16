from django.db import models
from django.contrib.auth.models import User
from propiedades.models import Propiedad  #7

class Compra(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='compras_compras')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras_compras')
    fecha_compra = models.DateTimeField(auto_now_add=True)

    nombre = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} compró {self.propiedad.titulo}"
