from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator

CATEGORY_CHOICES = (

    ('laptops','Laptops'),
    ('desktops','Desktops'),
    ('television','Television'),
    ('mobiles','Mobiles'),
    ('tablets','Tablets'),
    ('ipads','Ipads'),
    ('printers','Printers'),
    ('camera','Camera'),
    ('headphones', 'Headphones')
)


class Gadget(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    image = models.ImageField(upload_to='gadget_images/', null=True, blank=True)
    quantity = models.IntegerField(default=0)


    def __str__(self):

        return f"{self.name}"
    

class ProfileUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[('owner','Owner'),('user','User')])

    def __str__(self):
        return f"{self.username}"
    
    
class Cart(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username}"
    

class CartItems(models.Model):

    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    gadget = models.ForeignKey(Gadget, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(validators = [MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity}"
    

class Newsletter(models.Model):
    email = models.EmailField(unique = True)

    def __str__(self):
        return f"{self.email}"
    

    


