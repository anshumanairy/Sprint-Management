# Generated by Django 2.2 on 2019-07-23 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0024_auto_20190722_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='hleft',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='story',
            name='jleft',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='story',
            name='pleft',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='story',
            name='qleft',
            field=models.FloatField(default=0.0),
        ),
    ]
