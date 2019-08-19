from django.db import models
from django.forms import ModelForm
from datetime import date

class sprint(models.Model):
    name=models.CharField(max_length=100)
    holidays=models.IntegerField(default=0)
    sprint_start_date=models.DateField(blank=False)
    sprint_dev_end_date=models.DateField(blank=False)
    sprint_qa_end_date=models.DateField(blank=False)
    dev_working=models.IntegerField(default=0)
    qa_working=models.IntegerField(default=0)
    project_id=models.IntegerField()

    def __str__(self):
        return str(self.name)
