# Generated by Django 2.2 on 2019-08-13 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0068_auto_20190813_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sprint',
            old_name='pid',
            new_name='project_id',
        ),
    ]
