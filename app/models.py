from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Booking(models.Model):
    pickup = models.CharField(max_length=255,null=True, blank=True)
    drop = models.CharField(max_length=255 ,null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15 ,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)  # Distance can be null if not calculated

    def __str__(self):
        return f"{self.name} - {self.date}"

