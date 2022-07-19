from datetime import date, datetime
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum

from recon.models import Commision
from recon.models import Exchange

from .forms import CommisionForm, VehicleForm, ExpenseForm, Recondition_Form
from recon.models import Vehicle, Expenses, Comment, Order, Recondition,CustomUser,Photos, Category as Type

# Create your views here.

class Homepage(TemplateView):
    template_name = "recondition/homepage.html"

    def get(self, request, *args, **kwagrs):
        com = Comment.objects.filter(vehicle__user = request.user).filter(seen = False)
        print(com)
        # Purchase Report
        purchase = Vehicle.objects.filter(user = request.user).order_by('-purchase_date').aggregate(Sum('cost_price'))

        # sales report
        sale = Vehicle.objects.filter(user = request.user).filter(sold_status = True).order_by('-sold_date').aggregate(Sum('sold_price'))

        # expenses report
        expenses = Expenses.objects.filter(recondition = request.user).order_by('-date').aggregate(Sum('cost'))

        dist =  {
            'vehicle':Vehicle.objects.filter(user = request.user)[:6],
            'com':com[:5],
            'purchase':purchase,
            'sale':sale,
            'expenes':expenses,
            'vehicle_c':Vehicle.objects.filter(user = request.user).count(),
            'order':Order.objects.all().order_by('-id')[:5],
            'cmt_count':Comment.objects.filter(vehicle__user = request.user).filter(seen = False).count()
        }
        return render(request, self.template_name, dist)
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        vehi = Vehicle.objects.filter(name__icontains = name)

        dist = {
            'vehi':vehi
        }
        return render(request, 'recondition/search.html', dist) 
    
# Vehicle Views
class VehicleShow(TemplateView):
    template_name = "recondition/vehicle.html"

    def get(self, request, *args, **kwagrs):

        dist =  {
            'vehicle':Vehicle.objects.filter(user = request.user)
        }
        return render(request, self.template_name, dist)
    
   

# Add Vehicle Views
class Addvehicle(TemplateView):
    template_name = "recondition/addVehicle.html"

    def get(self, request, *args, **kwagrs):
        form = VehicleForm()
        form.fields['purchase_date'].initial = date.today()
        dist =  {
            'form':form
        }
        return render(request, self.template_name, dist)
    
    def post(self, request, *args, **kwargs):
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            saveit = form.save(commit=False)
            saveit.user = request.user
            form.save()
            messages.success(request, "Successfully Added your Vehicle")
            return HttpResponseRedirect(reverse('recond:addVehicleImage', args=[saveit.id]))

        else:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:vehicle'))  


# Add vehicle Image
def addVehicleImage(request, id):
    template_name = "recondition/addVehicleImage.html"
    vehicles = Vehicle.objects.get(id = id)
    print(vehicles)
    form = VehicleForm()
    
    dist =  {
        'form':form,
        'vehicle':vehicles
    }
  
    if request.method == 'POST':
        try:
            vehicles.image = request.FILES['image']
            images = request.FILES.getlist("file[]")
            vehicles.save()
            for img in images:
                image = Photos(vehicle = vehicles, image= img)
                image.save()
            messages.success(request, "Successfully Updated your Vehicle")
            return HttpResponseRedirect(reverse('recond:vehicle'))
            
        except:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:addVehicleImage', args=[id]))      
    return render(request, template_name, dist)

# Edit Vehicle Views
def Editvehicle(request, id):
    template_name = "recondition/editVehicle.html"
    vehicles = Vehicle.objects.get(id = id)
    print(vehicles)
    form = VehicleForm()
    form.fields['name'].initial = vehicles.name
    form.fields['cost_price'].initial = vehicles.cost_price
    form.fields['type'].initial = vehicles.type
    form.fields['plate_no'].initial = vehicles.plate_no
    form.fields['purchase_date'].initial = vehicles.purchase_date
    form.fields['showing_price'].initial = vehicles.showing_price
    form.fields['maintainance_cost'].initial = vehicles.maintainance_cost
    form.fields['maintainance_detail'].initial = vehicles.maintainance_detail
    form.fields['book_no'].initial = vehicles.book_no
    form.fields['insurance'].initial = vehicles.insurance
    form.fields['run_km'].initial = vehicles.run_km
    form.fields['modal'].initial = vehicles.modal
  
    
    dist =  {
        'form':form,
        'vehicle':vehicles
    }
  
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance = vehicles)
        if form.is_valid():

            form.save()
            images = request.FILES.getlist("file[]")
            vehicles.save()
            for img in images:
                image = Photos(vehicle = vehicles, image= img)
                image.save()
            messages.success(request, "Successfully Updated your Vehicle")
            return HttpResponseRedirect(reverse('recond:vehicle'))

        else:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:vehicle'))      
    return render(request, template_name, dist)
    
def deleteImage(request, id):
    imag = Photos.objects.get(id = id)
    imag.delete()
    messages.success(request, 'Deteled Images')
    return HttpResponseRedirect(reverse('recond:editvehicle', args=[imag.vehicle.id]))
#
# Delete Vehicle

def deleteVehicle(request, id):
    vehi = Vehicle.objects.get(id = id)
    try:
        vehi.delete()
        messages.success(request, "Successfully Deleted Vehicle")
    except:
        messages.success(request, "Successfully Deleted Vehicle")
    return HttpResponseRedirect(reverse('recond:vehicle'))





# Expenses Views
class Expenseshow(TemplateView):
    template_name = "recondition/expenses.html"
   
    def get(self, request, *args, **kwagrs):
        expenses = Expenses.objects.filter(recondition=request.user)
        exp_cost = Expenses.objects.filter(recondition = request.user).order_by('-date').aggregate(Sum('cost'))
        form = ExpenseForm()
        form.fields['date'].initial = date.today()
        dist =  {
            'form':form,
            'expenses': expenses,
            'cost':exp_cost
        }
        return render(request, self.template_name, dist)
    
    def post(self, request, *args, **kwargs):
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            saveit = form.save(commit=False)
            saveit.recondition = request.user
            form.save()
            messages.success(request, "Successfully Added your Expenses")
            return HttpResponseRedirect(reverse('recond:expense'))

        else:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:expense'))



# Sales Views
class Sales(TemplateView):
    template_name = "recondition/sales.html"
    # start = datetime.now() - datetime.timedelta(30)
    
    def get(self, request, *args, **kwagrs):
        sale = Vehicle.objects.filter(user = request.user).filter(sold_status = True).order_by('-sold_date')
        total_sale = sale.aggregate(Sum('sold_price'))

        dist =  {
            'sale':sale,
            'total_sale':total_sale,
            'type':Type.objects.all(),

        }
        return render(request, self.template_name, dist)
    
    def post(self, request, *args, **kwargs):
        start = request.POST['start']
        end = request.POST['end']
        print(start, end)
        type = request.POST['type']
        try:
            if type == 'all':
                sale = Vehicle.objects.filter(user = request.user).filter(sold_status = True).filter(sold_date__gte=start, sold_date__lte=end).order_by('-sold_date')
                tt = "All"
            else:
                sale = Vehicle.objects.filter(user = request.user).filter(sold_status = True).filter(sold_date__gte=start, sold_date__lte=end).order_by('-sold_date').filter(type_id = type)
                tt = Type.objects.get(id = type).name
            total_sale = sale.aggregate(Sum('sold_price'))
        
            dist =  {
                'sale':sale,
                'start':start,
                'end':end,
                'total_sale':total_sale,
                'type':Type.objects.all(),
                'tt':tt
            }
            messages.success(request, "Showing Your Records.....")
            return render(request, self.template_name, dist)

        except:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:sale'))

# Purchase Views
class Purchase(TemplateView):
    template_name = "recondition/purchase.html"

    def get(self, request, *args, **kwagrs):
        purchase = Vehicle.objects.filter(user = request.user).order_by('-purchase_date')
        total_purchase = purchase.aggregate(Sum('cost_price'))
        dist =  {
            'purchase':purchase,
            'total_purchase':total_purchase,
            'type':Type.objects.all(),

        }
        return render(request, self.template_name, dist)
    
    def post(self, request, *args, **kwargs):
        start = request.POST['start']
        end = request.POST['end']
        print(start, end)
        type = request.POST['type']
        try:
            if type == 'all':
                sale = Vehicle.objects.filter(user = request.user).filter(purchase_date__gte=start, purchase_date__lte=end).order_by('-purchase_date')
                tt = 'All'
            else:
                sale = Vehicle.objects.filter(user = request.user).filter(purchase_date__gte=start, purchase_date__lte=end).order_by('-purchase_date').filter(type_id = type)
                tt = Type.objects.get(id = type).name
            total_purchase = sale.aggregate(Sum('cost_price'))

            dist =  {
                'purchase':sale,
                'start':start,
                'end':end,
                'total_purchase':total_purchase,
                'type':Type.objects.all(),
                'tt': tt
            }
            messages.success(request, "Showing Your Records.....")
            return render(request, self.template_name, dist)
        except:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:purchase'))


# Report Views
class Report(TemplateView):
    template_name = "recondition/report.html"

    def get(self, request, *args, **kwagrs):
        # Purchase Report
        purchase = Vehicle.objects.filter(user = request.user).order_by('-purchase_date')
        total_purchase = purchase.aggregate(Sum('cost_price'))
        total_maintainance = purchase.aggregate(Sum('maintainance_cost'))
        print(total_maintainance['maintainance_cost__sum'])
        # sales report
        sale = Vehicle.objects.filter(user = request.user).filter(sold_status = True).order_by('-sold_date')
        total_sale = sale.aggregate(Sum('sold_price'))

        # expenses report
        
        expenses = Expenses.objects.filter(recondition = request.user).order_by('-date')
        total_expenses = expenses.aggregate(Sum('cost'))

        # Profit
        profit = total_sale['sold_price__sum'] - total_expenses['cost__sum'] - total_maintainance['maintainance_cost__sum'] - total_purchase['cost_price__sum']
        dist =  {
            'purchase':purchase,
            'total_purchase':total_purchase,
            'sale':sale,
            'total_sale':total_sale,
            'total_maintainace':total_maintainance,
            'expenses':expenses,
            'total_expenses':total_expenses,
            'type':Type.objects.all(),
            'profit':profit
        }
        return render(request, self.template_name, dist)
    
    def post(self, request, *args, **kwargs):
        start = request.POST['start']
        end = request.POST['end']
        print(start, end)
        type = request.POST['type']
        # try:
        if type == 'all':
            # Purchase Report
            purchase = Vehicle.objects.filter(user = request.user).filter(purchase_date__gte=start, purchase_date__lte=end).order_by('-purchase_date')
            # Sale Report
            sale = Vehicle.objects.filter(user = request.user).filter(sold_status = True).filter(sold_date__gte=start, sold_date__lte=end).order_by('-sold_date')
            # expenses report
            expenses = Expenses.objects.filter(recondition = request.user).order_by('-date').filter(date__gte=start, date__lte=end)
            tt = 'All'
        else:
            # Purchase Report
            purchase = Vehicle.objects.filter(user = request.user).filter(purchase_date__gte=start, purchase_date__lte=end).order_by('-purchase_date').filter(type_id = type)
            # Sale Report
            sale = Vehicle.objects.filter(user = request.user).filter(sold_status = True).filter(sold_date__gte=start, sold_date__lte=end).order_by('-sold_date').filter(type_id = type)
            # expenses report
            expenses = Expenses.objects.filter(recondition = request.user).order_by('-date').filter(date__gte=start, date__lte=end)
            tt = Type.objects.get(id = type).name
        total_purchase = purchase.aggregate(Sum('cost_price'))
        total_maintainance = purchase.aggregate(Sum('maintainance_cost'))
    

    
        total_sale = sale.aggregate(Sum('sold_price'))

    
        total_expenses = expenses.aggregate(Sum('cost'))
        # Profit
        try:
            if total_maintainance['maintainance_cost__sum']:
                profit = total_sale['sold_price__sum'] - total_expenses['cost__sum'] - total_maintainance['maintainance_cost__sum'] - total_purchase['cost_price__sum']
            else:
                profit = total_sale['sold_price__sum'] - total_expenses['cost__sum'] -  total_purchase['cost_price__sum']
        except:
            profit = 0
            
        dist =  {
            'start':start,
            'end':end,
            'purchase':purchase,
            'total_purchase':total_purchase,
            'sale':sale,
            'total_sale':total_sale,
            'expenses':expenses,
            'total_expenses':total_expenses,
            'total_maintainace':total_maintainance,
            'type':Type.objects.all(),
            'tt':tt,
            'profit':profit

        }
        return render(request, self.template_name, dist)
        # except:
        #     return HttpResponseRedirect(reverse('recond:report'))


        
# Order Views
class OrderShow(TemplateView):
    template_name = "recondition/order.html"

    def get(self, request, *args, **kwagrs):
        form = VehicleForm()
        order = Order.objects.filter(vehicle__user = request.user)
        dist =  {
            'form':form,
            'order':order
        }
        return render(request, self.template_name, dist)
    
    def post(self, request, *args, **kwargs):
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            saveit = form.save(commit=False)
            saveit.user = request.user
            form.save()
            messages.success(request, "Successfully Added your Vehicle")
            return HttpResponseRedirect(reverse('recond:order'))

        else:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:order'))

# Comment Views
class CommentShow(TemplateView):
    template_name = "recondition/comment.html"

    def get(self, request, *args, **kwagrs):
        form = VehicleForm()
        com = Comment.objects.filter(vehicle__user = request.user).order_by('-id')
        for i in com:
            i.seen = True
            i.save()
        dist =  {
            'form':form,
            'com':com
        }
        return render(request, self.template_name, dist)
    
   


def addToSold(request, id):
    vech = Vehicle.objects.get(id = id)
    dates = date.today()
    print(dates)
    dist = {
        'vehicle':vech,
        'date':dates
    }
    if request.method == 'POST':
        vech.sold_status = True
        vech.sold_date = request.POST['date']
        vech.sold_price = request.POST['price']

        vech.save()
        messages.success(request, "Successfully added to sold")
    return render(request, 'recondition/addToSold.html', dist)

class Profile(TemplateView):
    template_name = "recondition/profile.html"

    def post(self, request, *args, **kwargs):
        use = CustomUser.objects.get(id = request.user.id)
        use.first_name = request.POST['first_name']
        use.last_name = request.POST['last_name']
        use.email = request.POST['email']
        use.save()
        messages.success(request, "Successfully Updated Your Profile")
        
        return HttpResponseRedirect(reverse('recond:profile'))

class Rec_Profile(TemplateView):
    template_name = "recondition/rec_profile.html"

    def get(self, request, *args, **kwargs):
        form = Recondition_Form()
        rec = Recondition.objects.get(admin = request.user)
        form.fields['recondition_name'].initial = rec.recondition_name
        form.fields['number'].initial = rec.number
        form.fields['Temporary_address'].initial = rec.Temporary_address
        form.fields['District'].initial = rec.District
        form.fields['long'].initial = rec.long
        form.fields['lat'].initial = rec.lat
        dist = {
            'form':form,
            'rec':rec
        }
        return render(request, self.template_name, dist)
       
    def post(self, request, *args, **kwargs):
        rec = Recondition.objects.get(admin = request.user)
        form = Recondition_Form(request.POST, request.FILES, instance = rec)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated Your Profile")
            return HttpResponseRedirect(reverse('recond:rec_profile'))

        else:
            messages.success(request, "Something went wrong")
            return HttpResponseRedirect(reverse('recond:rec_profile')) 
       
class CommisionV(TemplateView):
    template_name = "recondition/commision.html"

    def get(self, request, *args, **kwargs):
        form = CommisionForm()
        vehi = Vehicle.objects.filter(sold_status = False).filter(user = request.user)
        com = Commision.objects.filter(vehicle__user = request.user)
        dist = {
            'form':form,
            'commision':com,
            'vehi':vehi
        }
        return render(request, self.template_name, dist)

    def post(self, request, *args, **kwargs):
        veh = Vehicle.objects.get(id = request.POST['vehicle'])
        rate = request.POST['rate']

        Commision.objects.create(vehicle = veh, rate = rate)
        
        messages.success(request, "Successfully Added Commision Vehicle ")
        return HttpResponseRedirect(reverse('recond:commision'))


def exchangeView(request):

    exchange = Exchange.objects.filter(vehicle__user = request.user)
    count = exchange.count()
    cc = {
        'exchange':exchange,
        'count':count
    }
    return render(request, "recondition/exchange.html", cc)