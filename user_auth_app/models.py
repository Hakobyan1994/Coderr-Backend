from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    PROFILE_TYPES = [
        ('business', 'Geschäftsprofil'),
        ('customer', 'Kundenprofil'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=PROFILE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)