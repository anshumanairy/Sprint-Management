from django import forms
from arc.models.register_mod import register
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ('username','email')
        widgets={
            'email': forms.EmailInput(attrs={'disabled': True}),
        }


class registerform(forms.ModelForm):

    class Meta():
        model = register
        fields = ('name','html','php','java','qa','roles','empid')
        widgets={
            'empid': forms.NumberInput(attrs={'disabled': True}),
        }
