# Generated by Django 2.1.7 on 2019-06-26 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0041_auto_20190626_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dev_working',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='qa_working',
            field=models.IntegerField(default=0),
        ),
    ]
