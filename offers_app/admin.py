from django.contrib import admin
from .models import Offer, OfferDetail

class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 1  # gibt eine leere Eingabezeile zusätzlich an
    fields = ["offer_type", "title", "price", "delivery_time_in_days", "revisions", "features"]
    readonly_fields = []

class OfferAdmin(admin.ModelAdmin):
    exclude = ["min_price", "min_delivery_time"]
    list_display = ["title", "creator", "created_at", "updated_at",'min_price','min_delivery_time']
    list_filter = ["creator", "created_at"]
    search_fields = ["title", "description", "creator__username"]
    inlines = [OfferDetailInline]

admin.site.register(Offer, OfferAdmin)

class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ["offer", "offer_type", "price", "delivery_time_in_days"]
    list_filter = ["offer_type", "delivery_time_in_days"]
    search_fields = ["offer__title", "title"]

admin.site.register(OfferDetail, OfferDetailAdmin)