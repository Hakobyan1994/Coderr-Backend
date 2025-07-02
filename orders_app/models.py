from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
     customer_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='customer_orders')
     business_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='business_user')
     title=models.CharField(max_length=200)
     revisions = models.IntegerField()
     delivery_time_in_days = models.IntegerField()
     price=models.IntegerField()
     features = models.JSONField(default=list)
     offer_type = models.CharField(max_length=20)
     status = models.CharField(max_length=200, default='in_progress')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)


     def __str__(self):
          return self.title
     

 