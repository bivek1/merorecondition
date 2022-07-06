from django.shortcuts import render
from django.views.generic import TemplateView, View
from recon.models import Vehicle
from recon.models import Recondition, CustomUser, Comment, Expenses, Order, Blog
from .forms import NormalForm, ReconditionForm, BlogForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
class Homepage(TemplateView):
    template_name = "owner/homepage.html"

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
            'vehicle':Vehicle.objects.filter(user = request.user),
            'com':com[:5],
            'purchase':purchase,
            'sale':sale,
            'expenes':expenses,
            'vehicle_c':Vehicle.objects.filter(user = request.user).count(),
            'order':Order.objects.all().order_by('-id')[:5],
            'cmt_count':Comment.objects.filter(vehicle__user = request.user).filter(seen = False).count()
        }

        return render(request, self.template_name, dist)

class ReconditionView(View):
    template_name = "owner/recondition.html"
    def get(self, request, *args, **kwagrs):

        dist =  {
            'recondition':Recondition.objects.all()
        }
        return render(request, self.template_name, dist)

# Add Vehicle Views
class AddRecondition(TemplateView):
    template_name = "owner/addRecondition.html"

    def get(self, request, *args, **kwagrs):
        form = ReconditionForm()
        nform = NormalForm()
        dist =  {
            'form':form,
            'nform':nform
        }
        return render(request, self.template_name, dist)
    
    def post(self, request, *args, **kwargs):
        form = ReconditionForm(request.POST, request.FILES)
        number = request.POST['number']
        recondition_name = request.POST['recondition_name']
        Temporary_address = request.POST['Temporary_address']
        profile_pic = request.FILES['profile_pic']
        expiry_date = request.POST['expire_on']
        try:
            verified = request.POST['verified']
        except:
            verified = False
        
        if form.is_valid():
            user = CustomUser.objects.create_user(username = request.POST['email'], email = request.POST['email'], password = request.POST['password'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], user_type = "recondition")
            user.recondition.number=number
            user.recondition.recondition_name= recondition_name
            user.recondition.Temporary_address=Temporary_address
            user.recondition.profile_pic=profile_pic
            if verified:
                user.recondition.verified=True
            user.recondition.expiry_date=expiry_date
            
            user.save()
            messages.success(request, "Successfully Added Recondition")
            return HttpResponseRedirect(reverse('owner:reconditonOwner'))

        else:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('owner:reconditon')) 

def editRecondition(request, id):
    recond = Recondition.objects.get(id = id)
    form = ReconditionForm()
    nform = NormalForm()
    form.fields['number'].initial = recond.number
    form.fields['recondition_name'].initial = recond.recondition_name
    form.fields['Temporary_address'].initial = recond.Temporary_address
    form.fields['District'].initial = recond.District
    form.fields['verified'].initial = recond.verified
    form.fields['expire_on'].initial = recond.expire_on
    nform.fields['first_name'].initial = request.user.first_name
    nform.fields['last_name'].initial = request.user.last_name
    nform.fields['email'].initial = request.user.email

    
    template_name = "owner/editRecondition.html"

    dist =  {
        'form':form,
        'nform':nform,
        'recond':recond
    }
    return render(request, template_name, dist)

class AddBlog(View):
    template_name = "addBlog"

    def get(self, request, *args, **kwargs):
        nform = BlogForm(request.POST, request.FILES)
        dist =  {
            'nform':nform
        }
        return render(request, self.template_name, dist)