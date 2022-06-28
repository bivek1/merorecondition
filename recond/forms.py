from django import forms
from recon.models import Vehicle, Expenses, Recondition


class VehicleForm(forms.ModelForm):
 
    class Meta:
        model = Vehicle
        fields = ('name','type', 'cost_price', 'plate_no', 'purchase_date', 'showing_price', 'maintainance_cost', 'maintainance_detail',  'book_no' ,'insurance', 'run_km' , 'modal', 'image' )
        # labels = None
        labels = {
            'name':'Name of the Vehicle',
            'type':'Type of Vehicle',
            'cost_price':'Cost Price of Vehicle',
            'plate_no': 'Plate No. of Vehicle',
            'purchase_date': 'Purchase Date',
            'showing_price':'Showing Price',
            'maintainance_cost':'Maintainance Cost',
            'maintainance_detail' : 'Maintainance Details',
            'book_no':'Book No/ Bike No',
            'insurance' : 'Insurance Description',
            'run_km' : 'Total run Km',
            'modal': 'Vehicle Modal',
            'image':'Image of Vehicle',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control col-12 col-md-6', 'placeholder':'Name of Vehicle'}),
            'type':forms.Select(attrs={'class':'form-control col-12 col-md-6'}),
            'cost_price':forms.NumberInput(attrs={'class':'form-control col-12 col-md-6', 'placeholder':'2500000'}),
            'plate_no': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Ba 1 Pa 2101'}),
            'purchase_date': forms.DateInput(attrs={'type':'date','class':'form-control', 'placeholder':'Purchase Date'}),
            'showing_price':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Showing Cost'}),
            'maintainance_cost':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Maintainance Cost'}),
            'maintainance_detail' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Maintainance Details...'}),
            'book_no':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Any Bike Indenfication no.'}),
            'insurance' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Insurance Details'}),
            'run_km' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1200'}),
            'modal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Vehicle Modal'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    
    class Meta:
        model = Expenses
        fields = ('reason','cost')

        labels = {
            'cost':'Total Cost',
            'reason':'Reason of Expenses',
        }

        widgets = {
            'reason':forms.TextInput(attrs = {'class':'form-control col-12 col-md-6', 'placeholder':'Reason of Expenses'}),
            'cost':forms.NumberInput(attrs = {'class':'form-control col-12 col-md-6', 'placeholder':'Total Cost of Expenses'}),
        }

class Recondition_Form(forms.ModelForm):
    class Meta:
        model = Recondition
        fields = ('recondition_name', 'number', 'Temporary_address', 'District', 'profile_pic')

        widgets = {
            'recondition_name':forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Reason of Expenses'}),
            'number':forms.NumberInput(attrs = {'class':'form-control', 'placeholder':'Number'}),
            'Temporary_address':forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Temporary Address'}),
            'District':forms.TextInput(attrs = {'class':'form-control', 'placeholder':'District'}),
            'profile_pic':forms.FileInput(attrs = {'class':'form-control'}),
        }