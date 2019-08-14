# Generated by Django 2.2 on 2019-08-13 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0063_auto_20190812_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_id', models.IntegerField()),
                ('comment', models.TextField(max_length=10000)),
                ('name', models.CharField(max_length=200)),
                ('time_of_comment', models.DateTimeField(blank='False')),
            ],
        ),
    ]