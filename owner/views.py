from django.shortcuts import render
from django.views.generic import TemplateView, View
from recon.models import Vehicle
from recon.models import Recondition, CustomUser
from .forms import NormalForm, ReconditionForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
class Homepage(TemplateView):
    template_name = "owner/homepage.html"

    def get(self, request, *args, **kwagrs):

        dist =  {
            'vehicle':Vehicle.objects.filter(user = request.user)
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
        if form.is_valid():
            user = CustomUser.objects.create_user(username = request.POST['email'], email = request.POST['email'], password = request.POST['password'], first_name = request.POST['first_name'], last_name = request.POST['last_name'],user_type = "recondition")
            saveit = form.save(commit=False)
            saveit.admin = user

            saveit.save()
            messages.success(request, "Successfully Added Recondition")
            return HttpResponseRedirect(reverse('owner:reconditon'))

        else:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect(reverse('owner:reconditon')) 