from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','profile_pic']

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'selling_price', 'discounted_price', 'mobile_image', 
                    'display', 'processor', 'ram', 'storage', 'rear_camera', 'selfie_camera', 'battery', 
                    'camera_setup', 'is_5g_capable']
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display= ['id','user','product','quantity']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id','user','fullname','email', 'pincode', 'phone_number', 'address']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','mobile','quantity','order_at','status','final_price']