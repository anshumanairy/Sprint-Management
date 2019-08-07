from django.db import models
from django.forms import ModelForm
from datetime import date

class progress(models.Model):
    s_id = models.IntegerField()
    sdate = models.DateField()
    jd = models.CharField(max_length=20)
    status = models.CharField(max_length = 15)
    dname = models.CharField(max_length=20)
    actual = models.FloatField(default=0.0)
    left = models.FloatField(default=0.0)
    cl = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.jd)
