from django import forms
from recon.models import Recondition

class NormalForm(forms.Form):
    first_name = forms.CharField(max_length=200, label = "First Name" ,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'User First Name'}))
    last_name = forms.CharField(max_length=200, label = "Last Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'User Last Name'}))
    email = forms.EmailField(max_length=200, label = "Email", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    password = forms.CharField(max_length=200, label = "Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
   
class ReconditionForm(forms.ModelForm):
    
    class Meta:
        model = Recondition
        fields = (
            'recondition_name', 'number' , 'Temporary_address', 'District' ,'profile_pic', 'expire_on', 'verified'
        )
    
        widgets = {
            'recondition_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Recondition Name'}), 
            'number':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Number'}), 
            'Temporary_address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Temporary Address'}), 
            'District':forms.TextInput(attrs={'class':'form-control', 'placeholder':'District'}),
            'profile_pic':forms.FileInput(attrs={'class':'form-control'}),
            'expire_on':forms.DateInput(attrs={'type':'date','class':'form-control'}), 
        }