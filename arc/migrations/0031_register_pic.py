# Generated by Django 2.2 on 2019-07-25 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0030_project_mans'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='pic',
            field=models.ImageField(blank=True, upload_to='static/profile/pics'),
        ),
    ]