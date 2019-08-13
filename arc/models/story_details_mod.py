from django.db import models
from django.forms import ModelForm
from datetime import date

class story_details(models.Model):
    story_id = models.IntegerField()
    sprint_id = models.IntegerField()
    jira= models.CharField(max_length=20)

    dev_java = models.CharField(max_length=200)
    dev_php = models.CharField(max_length=200)
    dev_html = models.CharField(max_length=200)
    dev_qa = models.CharField(max_length=200)

    javas = models.IntegerField(default=0)
    phps = models.IntegerField(default=0)
    htmls = models.IntegerField(default=0)
    qas = models.IntegerField(default=0)

    ostatus = models.CharField(max_length=20)

    comments = models.TextField(max_length=10000)

    jactual = models.FloatField(default=0.0)
    pactual = models.FloatField(default=0.0)
    hactual = models.FloatField(default=0.0)
    qactual = models.FloatField(default=0.0)

    jleft = models.FloatField(default=0.0)
    pleft = models.FloatField(default=0.0)
    hleft = models.FloatField(default=0.0)
    qleft = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.story_id)