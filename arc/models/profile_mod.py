from django.db import models
from django.contrib.auth.models import User

class display_picture(models.Model):
    profile_picture = models.ImageField(upload_to='Profile', blank=True)
    idx1 = models.IntegerField()
