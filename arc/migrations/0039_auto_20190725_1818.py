# Generated by Django 2.2 on 2019-07-25 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0038_auto_20190725_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='pic',
            field=models.ImageField(blank=True, upload_to='newfolder'),
        ),
    ]
