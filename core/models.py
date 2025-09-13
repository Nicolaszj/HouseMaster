from django.db import models

class Propiedad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    metros_cuadrados = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    imagen = models.URLField(blank=True)  # 1

    def __str__(self):
        return self.titulo
