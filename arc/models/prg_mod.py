from django.db import models
from django.forms import ModelForm
from datetime import date

class prg(models.Model):
    s_id = models.IntegerField()
    sdate = models.DateField()
    edate = models.DateField()
    jd = models.CharField(max_length=20)
    status = models.CharField(max_length = 15)
    dname = models.CharField(max_length=20)
    days = models.IntegerField()
    actual = models.IntegerField()

    def __str__(self):
        return str(self.jd)
