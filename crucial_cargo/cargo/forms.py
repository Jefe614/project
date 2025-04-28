from django import forms
from .models import Cargo, CargoImage, Invoice
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CargoRegistrationForm(forms.ModelForm):

    class Meta:
        model = Cargo
        fields = ['description', 'destination', 'estimated_delivery']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your cargo...'}),
            'estimated_delivery': forms.DateInput(attrs={'type': 'date'}),
        }

class InvoiceGenerationForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['amount', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)