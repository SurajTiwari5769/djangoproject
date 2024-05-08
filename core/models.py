from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Color(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.id)

class Mobile(models.Model):
    CAMERA_SETUP_CHOICES = [
        ('One', 'Single'),
        ('Two', 'Double'),
        ('Three', 'Triple'),
        ('Four', 'Four'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField(default=0, null=True, blank=True)
    mobile_image = models.ImageField(upload_to='mobile_images')
    display = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    rear_camera = models.CharField(max_length=100, default='NA')  # Rear camera details
    selfie_camera = models.CharField(max_length=100, default='NA')  # Selfie camera details
    battery = models.CharField(max_length=100)
    camera_setup = models.CharField(max_length=20, choices=CAMERA_SETUP_CHOICES, default='Triple')
    is_5g_capable = models.BooleanField(default=False)
    colors = models.ManyToManyField(Color, default='NA')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)        
    product = models.ForeignKey(Mobile, on_delete=models.CASCADE)  
    color = models.ForeignKey(Color, on_delete=models.CASCADE, default = 1)   
    quantity = models.PositiveIntegerField(default=1)              

    def __str__(self):
        return str(self.id)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    pincode = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    
    def __str__(self):
        return self.fullname
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    final_price = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.id)