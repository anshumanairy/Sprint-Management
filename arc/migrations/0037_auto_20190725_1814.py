# Generated by Django 2.2 on 2019-07-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0036_auto_20190725_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='pic',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]