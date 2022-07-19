from django.urls import path
from .import views
app_name = "recond"

urlpatterns = [
    path('', views.Homepage.as_view(), name="homepage"),
    path('vehicles', views.VehicleShow.as_view(), name = "vehicle" ),
    path('addvehicle', views.Addvehicle.as_view(), name= "addvehicle"),
    path('add-vehicle-images/<int:id>', views.addVehicleImage, name = 'addVehicleImage'),
    path('expenses', views.Expenseshow.as_view(), name = "expense" ),
    path('sales', views.Sales.as_view(), name = "sale" ),
    path('purchase', views.Purchase.as_view(), name = "purchase" ),
    path('report', views.Report.as_view(), name = "report" ),
    path('orders', views.OrderShow.as_view(), name = "order" ),
    path('comment', views.CommentShow.as_view(), name = "comment" ),
    path('editVehicle/<int:id>', views.Editvehicle, name = "editvehicle"),
    path('deleteVehicle/<int:id>', views.deleteVehicle, name = "delete"),
    path('addSale/<int:id>', views.addToSold, name ="addSale"),
    path('profile', views.Profile.as_view(), name = "profile"),
    path('recondition-profile', views.Rec_Profile.as_view(), name = "rec_profile"),
    path('add-to-sold/<int:id>', views.addToSold, name = "addToSold"),
    path('deleteImage/<int:id>', views.deleteImage, name="deleteImage"),
    path('commision',views.CommisionV.as_view(), name = "commision"),
    path('exchange', views.exchangeView, name ="exchange"),

]