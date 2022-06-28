from itertools import product
from statistics import mode
from turtle import back
from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = (("owner", "owner"), ("recondition", 'recondition'), ("customer", 'customer'))
    user_type = models.CharField(default = "owner", choices = user_type_data, max_length = 20)
    email = models.EmailField(unique = True)
    
class Owner(models.Model):
    id = models.AutoField(primary_key = 1)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.username

class Recondition(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    number = models.BigIntegerField(blank= True, null = True)
    recondition_name = models.CharField(max_length=200)
    Temporary_address = models.CharField(max_length = 300)
    District = models.CharField(max_length = 50, default = 'Kathmandu')
    profile_pic = models.ImageField(upload_to = "Recondition", blank = True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    expire_on = models.DateField(blank= True, null = True)
   
    objects = models.Manager()
    
    def __str__(self):
        return self.admin.first_name

    
class Customer(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser,  on_delete=models.CASCADE)
    number = models.BigIntegerField(null=True)
    Temporary_address = models.CharField(max_length = 300)
    street = models.CharField(max_length = 200)
    District = models.CharField(max_length = 50)
    profile_pic = models.ImageField(upload_to = "Customer_Profile", blank = True)
    gender = models.CharField(max_length = 100, choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    ))
    objects = models.Manager()
    def __str__(self):
        return self.admin.email



class Category(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to ="category")
    objects = models.Manager()
    
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, related_name = "user_vehicle", on_delete= models.CASCADE)
    type = models.ForeignKey(Category, related_name="vehicle_category", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    cost_price = models.IntegerField()
    plate_no = models.CharField(max_length=50)
    maintainance_cost = models.IntegerField(blank=True, null =True)
    maintainance_detail = models.CharField(max_length=500, blank=True, null =True)
    purchase_date = models.DateField(blank=True)
    sold_date = models.DateField(blank=True, null =True)
    showing_price = models.IntegerField()
    sold_status = models.BooleanField(default=False)
    image = models.ImageField(upload_to = "vehicle", blank = True , null =True)
    sold_price = models.IntegerField(blank=True , null =True)
    remarks = models.CharField(max_length=1000, blank=True, null =True)
    book_no = models.CharField(max_length=200 , blank=True, null =True)
    insurance = models.CharField(max_length=1000, blank=True , null =True)
    run_km = models.IntegerField()
    modal = models.CharField(max_length = 200, blank=True, null =True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    cost = models.IntegerField()
    reason = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    recondition = models.ForeignKey(CustomUser, related_name="recondition_expenses", on_delete=models.CASCADE)

    def __str__(self):
        return self.reason

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    recondition = models.ForeignKey(CustomUser, related_name="recondition_transaction", on_delete=models.CASCADE)
    sales = models.BigIntegerField(blank=True)
    purchase = models.BigIntegerField(blank=True)
    vehicle = models.ForeignKey(Vehicle, related_name = "vechile_transaction", on_delete=models.CASCADE)

    def __str__(self):
        return self.recondition.first_name


class Comment(models.Model):
    id = models.AutoField(primary_key = True)
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, related_name="user_comment", on_delete=models.CASCADE, null = True, blank=True)
    vehicle = models.ForeignKey(Vehicle, related_name = "vehicle_comment", on_delete=models.CASCADE)
    objects = models.Manager()
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.comment


class Order(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=200)
    number = models.BigIntegerField()
    user = models.ForeignKey(CustomUser, related_name="user_order", on_delete= models.CASCADE, null = True, blank = True)
    address = models.CharField(max_length=200)
    vehicle = models.ForeignKey(Vehicle, related_name = "vehicle_order", on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    def __str__(self):
        return self.name


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "owner":
            Owner.objects.create(admin = instance)
        if instance.user_type == "recondition":
            Recondition.objects.create(admin = instance)
        if instance.user_type == "customer":
            Customer.objects.create(admin = instance)
       

@receiver(post_save, sender=CustomUser)
def post_save_receiver(sender, instance, **kwargs):
    if instance.user_type == "owner":
        instance.owner.save()
    if instance.user_type == "recondition":
        instance.recondition.save()
    if instance.user_type == "customer":
        instance.customer.save()
 
