from django.db import models
from django.forms import ModelForm
from datetime import date

class comments(models.Model):
    story_id = models.IntegerField()
    comment = models.TextField(max_length=10000)
    # name = models.CharField(max_length=200)
    user_id = models.IntegerField()
    time_of_comment = models.CharField(max_length=50,blank='False')

    def __str__(self):
        return str(self.story_id)
