from django.db import models
from django.forms import ModelForm
from datetime import date

class project(models.Model):
    name=models.CharField(max_length=100,default="Enter Name")
    def __str__(self):
        return str(self.name)
