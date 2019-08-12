from django.db import models
from django.forms import ModelForm
from datetime import date

class story(models.Model):
    sprint_id = models.IntegerField()
    story_name= models.CharField(max_length=200)
    description= models.URLField(blank=False)
    jira= models.CharField(max_length=20)

    def __str__(self):
        return str(self.jira)
