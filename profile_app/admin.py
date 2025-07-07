from django.contrib import admin
from  .models import BusinessProfile,CustomerProfile
from django import forms
# Register your models here.


class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "get_first_name", "get_last_name", "email", "tel", "location",'get_created']
    list_filter = ["user__date_joined","location"]
    search_fields = ["username", "first_name", "last_name", "email", "tel", "location"]
    readonly_fields = ["user_type"]
    exclude=['created_at']
    list_select_related = ["user"]

    @admin.display(ordering="user__first_name", description="first_name")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering="user__last_name", description="last_name")
    def get_last_name(self, obj):
        return obj.user.last_name

    @admin.display(ordering="user__date_joined", description="created_at")
    def get_created(self, obj):
        return obj.user.date_joined



admin.site.register(BusinessProfile,BusinessProfileAdmin)



class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["username","get_first_name","get_last_name", "email","get_created",]
    list_filter = ["user__date_joined"]
    search_fields = ["username", "user__first_name","user__last_name","email",]
    readonly_fields = ["user_type"]
    list_select_related = ["user"]
    exclude=['created_at']


    @admin.display(ordering="user__first_name", description="first_name")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering="user__last_name", description="last_name")
    def get_last_name(self, obj):
        return obj.user.last_name

    @admin.display(ordering="user__date_joined", description="created_at")
    def get_created(self, obj):
        return obj.user.date_joined
    
admin.site.register(CustomerProfile,CustomerProfileAdmin)