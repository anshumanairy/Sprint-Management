# Generated by Django 2.2 on 2019-07-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0021_auto_20190717_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='prg',
            name='actual',
            field=models.FloatField(default=0.0),
        ),
    ]