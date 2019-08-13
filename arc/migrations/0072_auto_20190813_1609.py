# Generated by Django 2.2 on 2019-08-13 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0071_remove_story_details_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='brief_description',
            field=models.CharField(default=None, max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='story',
            name='overall_status',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]
