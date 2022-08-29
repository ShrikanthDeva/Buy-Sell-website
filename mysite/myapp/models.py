from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class product(models.Model):
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('myapp:products')
    seller_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    desc = models.CharField(max_length=200)
    image = models.ImageField(blank=True,upload_to='images')

class OrderDetail(models.Model):
    customer_name = models.CharField(max_length=200)
    prod = models.ForeignKey(to='product',on_delete=models.PROTECT)
    amount = models.IntegerField()
    checkout_session_id = models.CharField(max_length=200,null=True) 
    stripe_payment_intent = models.CharField(max_length=200,null=True)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)


