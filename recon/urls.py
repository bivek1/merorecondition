from django.urls import path
from .import views

app_name = "recon"


urlpatterns = [
    path('', views.Homepage.as_view(), name = "homepage"), 
    path('login', views.loginPage, name = "login"), 
    path('logout', views.logoutPage, name = "logout"),
    path('vechileDetails/<int:id>', views.vehicleDetail, name = "vehicleD"),
    path('allvehicle', views.allVehicle.as_view(), name = "allVehicle"),
    path('all-recondition-house', views.allHouse.as_view(), name = "allHouse"),
    path('recondition-details/<int:id>', views.reconditionD, name = "reconditionD"),
    path('about-merorecondition.com', views.About.as_view(), name = "about"),
    path('contact-merorecondition.com', views.Contact.as_view(), name = "contact"),
    path('order/<int:id>', views.order, name = "order"),
]
