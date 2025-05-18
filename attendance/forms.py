from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'address', 'contact_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-input'}),
        }
