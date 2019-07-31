from django.db import models
from django.contrib.auth.models import User

role = (
    ('dev','Developer'),
    ('man','Manager'),
)

class register(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    uname = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    roles = models.CharField(max_length=4, choices=role, default="Roles")

    html = models.BooleanField(default=False)
    php = models.BooleanField(default=False)
    java = models.BooleanField(default=False)
    qa = models.BooleanField(default=False)

    empid = models.IntegerField()

    def __str__(self):
        return self.user.username
