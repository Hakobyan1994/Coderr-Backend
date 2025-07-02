from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Offer(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.FileField(upload_to='offer_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    min_delivery_time = models.PositiveIntegerField(default=7)

    def __str__(self):
        return self.title
    
class OfferDetail(models.Model):
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time_in_days = models.PositiveIntegerField(default=0)
    revisions = models.IntegerField(default=-1)
    features = models.JSONField(default=list)    


    def __str__(self):
        return f"{self.offer.title} ({self.offer_type})"    