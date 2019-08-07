from django import forms
from arc.models.register_mod import user_detail
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ('username','email')
        widgets={
            'email': forms.EmailInput(attrs={'readonly': True}),
        }


class registerform(forms.ModelForm):

    class Meta():
        model = user_detail
        fields = ('name','html','php','java','qa','roles','empid')
        widgets={
            'name': forms.TextInput(attrs={'readonly': True}),
            'empid': forms.NumberInput(attrs={'readonly': True}),
        }
