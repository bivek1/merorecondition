from django.urls import path
from .import views
app_name = "customer"

urlpatterns = [
    path('', views.Homepage.as_view(), name="homepage"),
]