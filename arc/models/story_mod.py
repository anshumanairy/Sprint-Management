from django.db import models
from django.forms import ModelForm
from datetime import date

class story(models.Model):
    sprint_id = models.IntegerField()
    story_name= models.CharField(max_length=200)
    description= models.URLField(blank=False)
    jira= models.CharField(max_length=20)

    dev_java = models.CharField(max_length=200)
    dev_php = models.CharField(max_length=200)
    dev_html = models.CharField(max_length=200)
    dev_qa = models.CharField(max_length=200)

    javas = models.IntegerField(default=0)
    phps = models.IntegerField(default=0)
    htmls = models.IntegerField(default=0)
    qas = models.IntegerField(default=0)

    jstat = models.CharField(max_length=20)
    pstat = models.CharField(max_length=20)
    hstat = models.CharField(max_length=20)
    qstat = models.CharField(max_length=20)

    jactual = models.IntegerField(default=0)
    pactual = models.IntegerField(default=0)
    hactual = models.IntegerField(default=0)
    qactual = models.IntegerField(default=0)

    def __str__(self):
        return str(self.jira)
