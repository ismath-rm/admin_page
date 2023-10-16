from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_active",
            "is_superuser"
            ]

        widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'is_active': forms.CheckboxInput (attrs={'class': 'form-check-input'}),
        'is_superuser': forms.CheckboxInput (attrs={'class': 'form-check-input'}),
        }

