from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Category, Order, Recondition, Vehicle, Comment
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login
# Create your views here.
class Homepage(TemplateView):

    template_name = "homepage.html"

    def get(self, request, *agrs,**kwargs):
        category = Category.objects.all()[:6]
        latest = Vehicle.objects.all()[:6]
        houses = Recondition.objects.all()[:6]
        rec = Recondition.objects.all()[:6]
        dist = {
            'category':category,
            'lastest':latest,
            'hot':latest,
            'houses':houses,
            'rec':rec
            
        }
        return render(request,self.template_name, dist)

def loginPage(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)
            if user.user_type == "owner":
                return HttpResponseRedirect(reverse('owner:homepage'))
            elif user.user_type == "recondition":
                return HttpResponseRedirect(reverse('recond:homepage'))
            else:
                return HttpResponseRedirect(reverse('customer:homepage'))
            

            
        else:
            messages.error(request, "Username or Password does not match")


    return render(request, "loginPage.html")

def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse('recon:homepage'))
    


def vehicleDetail(request, id):
    vehicle = Vehicle.objects.get(id = id)
    comments = Comment.objects.filter(vehicle = vehicle)
    dist = {
        'vehicle':vehicle,
        'comment':comments
    }
    if request.method == 'POST':
        comment = request.POST['comment']
        if request.user.is_authenticated:
            Comment.objects.create(comment = comment, user = request.user, vehicle = vehicle)
        else:
            Comment.objects.create(comment = comment, vehicle = vehicle)
        
    return render(request, "vehicleD.html", dist)


class allVehicle(View):
    template_name = "vehicle.html"
    def get(self, request, *args, **kwargs):
        dist = {
            'vehicle':Vehicle.objects.all().order_by('-id')
        }
        return render(request, self.template_name, dist)



class allHouse(View):
    template_name = "house.html"

    def get(self, request, *args, **kwargs):
        dist = {
            'house':Recondition.objects.all().order_by('-id')
        }
        return render(request, self.template_name, dist)


def reconditionD(request, id):
    tem = "recondition.html"
    recon = Recondition.objects.get(id = id)
    vehicle = Vehicle.objects.filter(user= recon.admin).order_by('-id')[:6]
    all_vehicle = Vehicle.objects.filter(user = recon.admin)
    dist = {
        'recon': recon,
        'vehicle':vehicle,
        'all_vehicle': all_vehicle
    }

    return render(request, tem, dist)

class About(TemplateView):
    template_name= "about.html"

class Contact(TemplateView):
    template_name= "contact.html"

def order(request, id):
    vehicle = Vehicle.objects.get(id = id)
    dist = {
        'vehicle':vehicle
    }
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        address = request.POST['address']
        if name == ""  or number == "" or address == "":
            messages.error(request,"Please Add All the Information")
        else:
            if request.user.is_authenticated:
                Order.objects.create(name = name, number= number, address = address, user = request.user)
            else:
                Order.objects.create(name = name, number= number, address = address)
            messages.success(request, "Succesfully Ordered. Wait for the Call")
    return render(request, 'order.html', dist)