# Generated by Django 2.1.7 on 2019-06-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0059_auto_20190628_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='planned',
            field=models.IntegerField(default=0),
        ),
    ]
