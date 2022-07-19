from django.contrib import admin
from .models import Exchange, Contact, CustomUser,Blog, Order, Owner, Recondition ,Commision, Customer, Vehicle, Category, Transaction, Expenses
# Register your models here.
admin.site.register(Owner)
admin.site.register(Recondition)
admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Expenses)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(Blog)
admin.site.register(Commision)
admin.site.register(Exchange)
admin.site.register(Contact)