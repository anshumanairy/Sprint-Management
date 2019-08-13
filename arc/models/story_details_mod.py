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

    assigned_java_points = models.IntegerField(default=0)
    assigned_php_points = models.IntegerField(default=0)
    assigned_html_points = models.IntegerField(default=0)
    assigned_qa_points = models.IntegerField(default=0)

    ostatus = models.CharField(max_length=20)

    java_points_done = models.FloatField(default=0.0)
    php_points_done = models.FloatField(default=0.0)
    html_points_done = models.FloatField(default=0.0)
    qa_points_done = models.FloatField(default=0.0)

    java_points_left = models.FloatField(default=0.0)
    php_points_left = models.FloatField(default=0.0)
    html_points_left = models.FloatField(default=0.0)
    qa_points_left = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.story_id)
