# Generated by Django 2.2 on 2019-07-17 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0013_auto_20190716_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
    ]
