from django.urls import path
from .import views
app_name = "owner"

urlpatterns = [
    path('', views.Homepage.as_view(), name="homepage"),
    path('recondition', views.ReconditionView.as_view(), name ="reconditon"),
    path('addrecondition', views.AddRecondition.as_view(), name ="addRecondition")
]