# Generated by Django 2.2 on 2019-07-24 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0029_project_devs'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='mans',
            field=models.CharField(default=None, max_length=1000),
            preserve_default=False,
        ),
    ]
