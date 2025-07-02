from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Review(models.Model):
    business_user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_reviews')
    reviewer=models.ForeignKey(User, on_delete=models.CASCADE,related_name='given_reviews')
    rating=models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        unique_together = ('business_user', 'reviewer')
        ordering = ['-updated_at']

