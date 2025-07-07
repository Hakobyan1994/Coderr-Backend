from django.db import models
from django.contrib.auth.models import User
# Create your models here.

USER_TYPE_CHOICES = [
    ('business', 'Geschäftsprofil'),
    ('customer', 'Kundenprofil'),
]


class BusinessProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='business')
    username=models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    tel = models.CharField(max_length=25)
    location = models.CharField(max_length=150)
    description=models.TextField(blank=True)
    working_hours = models.CharField(max_length=255)
    created_at = models.CharField(max_length=200)
    email=models.EmailField(blank=True)
    
class CustomerProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', blank=True)
    created_at = models.CharField(max_length=200)
    email=models.EmailField(blank=True)
    username=models.CharField(max_length=100)
    







    