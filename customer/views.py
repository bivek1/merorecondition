from django.shortcuts import render
from django.views.generic import TemplateView
from recon.models import Vehicle
# Create your views here.

class Homepage(TemplateView):
    template_name = "customer/homepage.html"

    def get(self, request, *args, **kwagrs):

        dist =  {
            'vehicle':Vehicle.objects.filter(user = request.user)
        }
        return render(request, self.template_name, dist)