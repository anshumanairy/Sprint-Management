from django.db import models
from django.forms import ModelForm
from datetime import date

class project_details(models.Model):
    project_id = models.IntegerField()
    creator = models.CharField(max_length=150)
    devs = models.CharField(max_length=1000)
    mans = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.creator)
