from django.db import models

class user_sprint_detail(models.Model):
    uname = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    sprint_id = models.IntegerField()
    roles = models.CharField(max_length=4)

    html = models.BooleanField(default=False)
    php = models.BooleanField(default=False)
    java = models.BooleanField(default=False)
    qa = models.BooleanField(default=False)

    velocity_factor_html = models.FloatField(default=0)
    velocity_factor_php = models.FloatField(default=0)
    velocity_factor_java = models.FloatField(default=0)
    velocity_factor_qa = models.FloatField(default=0)

    available_bandwidth_java = models.IntegerField(default=0)
    available_bandwidth_php = models.IntegerField(default=0)
    available_bandwidth_html = models.IntegerField(default=0)
    available_bandwidth_qa = models.IntegerField(default=0)

    planned_leaves = models.IntegerField(default=0)
    unplanned_leaves = models.IntegerField(default=0)

    story_points_java = models.IntegerField(default=0)
    story_points_php = models.IntegerField(default=0)
    story_points_html = models.IntegerField(default=0)
    story_points_qa = models.IntegerField(default=0)

    delta_java = models.IntegerField(default=0)
    delta_php = models.IntegerField(default=0)
    delta_html = models.IntegerField(default=0)
    delta_qa = models.IntegerField(default=0)

    def __str__(self):
        return str(self.uname)
