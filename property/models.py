from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='properties')

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=100)   # Venta / Arriendo
    area = models.FloatField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    status = models.CharField(max_length=50)  # Disponible, Vendida, etc.
    city = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    address = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.city}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=150, blank=True)
    is_cover = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_cover', 'id']  # portada primero

    def __str__(self):
        return f"Foto de {self.property.title}"
