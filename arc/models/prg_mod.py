from django.db import models
from django.forms import ModelForm
from datetime import date

class progress(models.Model):
    story_id = models.IntegerField()
    work_date = models.DateField()
    jira_id = models.CharField(max_length=20)
    status = models.CharField(max_length = 15)
    dev_name = models.CharField(max_length=20)
    actual = models.FloatField(default=0.0)
    left = models.FloatField(default=0.0)
    calculated_left = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.jira_id)
