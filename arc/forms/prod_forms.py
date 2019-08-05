from django import forms
from arc.models.prod_mod import product
from django.contrib.auth import login,authenticate,logout,get_user_model

class productform(forms.ModelForm):
    # sprint_start_date= forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=('%m/%d/%Y',))
    # sprint_dev_end_date= forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=('%m/%d/%Y',))
    # sprint_qa_end_date= forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=('%m/%d/%Y',))

    class Meta:
        model=product
        fields = ['name','holidays']
