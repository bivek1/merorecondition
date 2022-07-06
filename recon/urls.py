from django.urls import path
from .import views

app_name = "recon"


urlpatterns = [
    path('', views.Homepage.as_view(), name = "homepage"), 
    path('login', views.loginPage, name = "login"), 
    path('logout', views.logoutPage, name = "logout"),
    path('vechileDetails/<slug:slug>', views.vehicleDetail, name = "vehicleD"),
    path('allvehicle', views.allVehicle.as_view(), name = "allVehicle"),
    path('all-recondition-house', views.allHouse.as_view(), name = "allHouse"),
    path('recondition-details/<slug:slug>', views.reconditionD, name = "reconditionD"),
    path('about-merorecondition.com', views.About.as_view(), name = "about"),
    path('contact-merorecondition.com', views.ContactV.as_view(), name = "contact"),
    path('order/<int:id>', views.order, name = "order"),
    path('category/<int:id>', views.categoryShow, name = "category"),
    path('Blog', views.BlogV, name = "blog"),
    path('blogDetails/<slug:slug>', views.blogDetails, name = "blogD"),
    path('earn', views.Earn.as_view(), name = "earn"),

]
