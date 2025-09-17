from django.db import models
from django.contrib.auth.models import User
from property.models import Property

class Visit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_time", "-created_at"]
        indexes = [
            models.Index(fields=["property", "date_time"]),
            models.Index(fields=["user", "date_time"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "property", "date_time"],
                name="uniq_visit_user_prop_datetime",
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.property.title} ({self.date_time})"
