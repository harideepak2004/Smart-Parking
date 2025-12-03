from django import forms
from .models import CompanyDetail

class CompanyDetailForm(forms.ModelForm):
    class Meta:
        model = CompanyDetail
        fields = ['name', 'email', 'phone', 'address', 'floors', 'slots']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your company name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'rows':3, 'placeholder': 'Enter your company address'}),
            'floors': forms.Select(attrs={'placeholder': 'Select number of floors'}),
            'slots': forms.Select(attrs={'placeholder': 'Select number of slots'}),
        }
