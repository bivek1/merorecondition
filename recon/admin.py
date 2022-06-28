from django.contrib import admin
from .models import CustomUser, Order, Owner, Recondition, Customer, Vehicle, Category, Transaction, Expenses
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
