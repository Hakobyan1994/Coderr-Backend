from django.contrib import admin
from .models import Review
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display=['business_user__username','reviewer__username','rating','created_at','description',  'updated_at']
    list_filter=['reviewer__username','created_at','rating']
    search_fields = ['business_user__username','reviewer__username']

admin.site.register(Review,ReviewAdmin)
