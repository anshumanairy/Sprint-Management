# Generated by Django 2.1.7 on 2019-06-26 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0019_remove_story_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='description',
            field=models.URLField(),
        ),
    ]
