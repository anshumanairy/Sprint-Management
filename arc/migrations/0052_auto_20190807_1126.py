# Generated by Django 2.2 on 2019-08-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0051_auto_20190807_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='qa_working',
            field=models.IntegerField(),
        ),
    ]
