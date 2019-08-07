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

    vfhtml = models.FloatField(default=0)
    vfphp = models.FloatField(default=0)
    vfjava = models.FloatField(default=0)
    vfqa = models.FloatField(default=0)

    abjava = models.IntegerField(default=0)
    abphp = models.IntegerField(default=0)
    abhtml = models.IntegerField(default=0)
    abqa = models.IntegerField(default=0)

    planned = models.IntegerField(default=0)
    unplanned = models.IntegerField(default=0)

    spjava = models.IntegerField(default=0)
    spphp = models.IntegerField(default=0)
    sphtml = models.IntegerField(default=0)
    spqa = models.IntegerField(default=0)

    djava = models.IntegerField(default=0)
    dphp = models.IntegerField(default=0)
    dhtml = models.IntegerField(default=0)
    dqa = models.IntegerField(default=0)

    def __str__(self):
        return str(self.uname)
