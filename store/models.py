from django.db import models
from django.conf import settings

# Create your models here.

class Customer(models.Model):
    MEMBERSHIP_USER = 'U'
    MEMBERSHIP_VENDOR = 'V'
  

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_USER, 'User'),
        (MEMBERSHIP_VENDOR, 'Vendor'),
       
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_USER)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

   
class Collection(models.Model):
    title =  models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name='products')
    stock = models.PositiveSmallIntegerField()
    description = models.TextField()
    vendor = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    STATUS_PROCESSING = 'P'
    STATUS_SUCCESS = 'S'
    STATUS_CHOICES = [
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_PROCESSING, 'Success'),
       
    ]
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PROCESSING)
    
    def __str__(self):
        return f'{self.product.title} {self.quantity}'
    