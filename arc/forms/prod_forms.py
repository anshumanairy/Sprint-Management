from django import forms
from arc.models.prod_mod import sprint
from django.contrib.auth import login,authenticate,logout,get_user_model

class sprintform(forms.ModelForm):

    class Meta:
        model=sprint
        fields = ['name','holidays']
