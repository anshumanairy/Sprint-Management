# Generated by Django 2.2 on 2019-08-19 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0084_remove_user_detail_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]