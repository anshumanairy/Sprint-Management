from django.db import models
from django.forms import ModelForm
from datetime import date

class product(models.Model):
    name=models.CharField(max_length=100,default="Enter Name")
    holidays=models.IntegerField(default=0)
    sprint_start_date=models.DateField(blank=False,default=date.today)
    sprint_dev_end_date=models.DateField(blank=False,default=date.today)
    sprint_qa_end_date=models.DateField(blank=False,default=date.today)
    dev_working=models.IntegerField(default=0)
    qa_working=models.IntegerField(default=0)
    pid=models.IntegerField() 

    def __str__(self):
        return str(self.name)
