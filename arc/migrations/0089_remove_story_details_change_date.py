# Generated by Django 2.2 on 2019-08-21 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0088_story_details_change_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story_details',
            name='change_date',
        ),
    ]