# Generated by Django 2.2 on 2019-07-26 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0043_remove_register_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='static/')),
            ],
        ),
    ]
