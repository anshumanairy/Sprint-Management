# Generated by Django 2.2 on 2019-07-15 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0004_auto_20190715_0844'),
    ]

    operations = [
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Enter Name', max_length=100)),
            ],
        ),
    ]