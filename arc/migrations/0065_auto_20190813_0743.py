# Generated by Django 2.2 on 2019-08-13 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0064_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='time_of_comment',
            field=models.CharField(blank='False', max_length=50),
        ),
    ]
