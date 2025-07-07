from django.contrib import admin
from .models import Order
# Register your models here.



class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "title", 
        "customer_user", 
        "business_user", 
        "offer_type",
        "price",
        "status",
        "delivery_time_in_days",
        "revisions",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "status",
        "offer_type",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "customer_user__username",
        "business_user__username",
        "offer_type",
        "status",
    ]

    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("User Informations", {
            "fields": ("customer_user", "business_user")
        }),
        ("Order details", {
            "fields": ("title", "offer_type", "price", "status")
        }),
        ("Additional details", {
            "fields": ("features", "revisions", "delivery_time_in_days")
        }),
        ("Timestamp", {
            "fields": ("created_at", "updated_at")
        }),
    )

admin.site.register(Order,OrderAdmin)    