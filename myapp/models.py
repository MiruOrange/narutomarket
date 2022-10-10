from email.policy import default
from django.db import models

# Create your models here.
class ProductModel(models.Model):
    pname = models.CharField(max_length=30, null=False)
    pprice = models.IntegerField(null = False)
    pimage = models.CharField(max_length=40, null=False)
    pdescription = models.TextField(null= False)

class OrderModel(models.Model):
    subtotal = models.IntegerField(null= False, default=0)
    shipping = models.IntegerField(null= False, default=0)
    grandtotal = models.IntegerField(null= False, default=0)
    customername = models.CharField(max_length=50)
    customerphone = models.CharField(max_length=50)
    customeremail = models.CharField(max_length=50)
    customeraddress = models.CharField(max_length=50)
    paytype = models.CharField(max_length=5, default='ATM')

class DetailModel(models.Model):
    dorder = models.ForeignKey('OrderModel', on_delete=models.CASCADE)
    pname = models.CharField(max_length=30, null=False)
    unitprice = models.IntegerField(null = False)
    quantity = models.IntegerField(null = False)
    dtotal = models.IntegerField(null = False)
    
