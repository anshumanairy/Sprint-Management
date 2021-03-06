# Generated by Django 2.2 on 2019-07-14 21:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='prg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.IntegerField()),
                ('sdate', models.DateField()),
                ('edate', models.DateField()),
                ('jd', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=15)),
                ('dname', models.CharField(max_length=20)),
                ('days', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Enter Name', max_length=100)),
                ('holidays', models.IntegerField(default=0)),
                ('sprint_start_date', models.DateField(default=datetime.date.today)),
                ('sprint_dev_end_date', models.DateField(default=datetime.date.today)),
                ('sprint_qa_end_date', models.DateField(default=datetime.date.today)),
                ('dev_working', models.IntegerField(default=0)),
                ('qa_working', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sprint_id', models.IntegerField()),
                ('story_name', models.CharField(max_length=200)),
                ('description', models.URLField()),
                ('jira', models.CharField(max_length=20)),
                ('dev_java', models.CharField(max_length=200)),
                ('dev_php', models.CharField(max_length=200)),
                ('dev_html', models.CharField(max_length=200)),
                ('dev_qa', models.CharField(max_length=200)),
                ('javas', models.IntegerField(default=0)),
                ('phps', models.IntegerField(default=0)),
                ('htmls', models.IntegerField(default=0)),
                ('qas', models.IntegerField(default=0)),
                ('jstat', models.CharField(max_length=20)),
                ('pstat', models.CharField(max_length=20)),
                ('hstat', models.CharField(max_length=20)),
                ('qstat', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=20)),
                ('roles', models.CharField(choices=[('dev', 'Developer'), ('man', 'Manager')], default='Roles', max_length=4)),
                ('html', models.BooleanField(default=False)),
                ('php', models.BooleanField(default=False)),
                ('java', models.BooleanField(default=False)),
                ('qa', models.BooleanField(default=False)),
                ('vfhtml', models.FloatField(default=0)),
                ('vfphp', models.FloatField(default=0)),
                ('vfjava', models.FloatField(default=0)),
                ('vfqa', models.FloatField(default=0)),
                ('abjava', models.IntegerField(default=0)),
                ('abphp', models.IntegerField(default=0)),
                ('abhtml', models.IntegerField(default=0)),
                ('abqa', models.IntegerField(default=0)),
                ('planned', models.IntegerField(default=0)),
                ('unplanned', models.IntegerField(default=0)),
                ('spjava', models.IntegerField(default=0)),
                ('spphp', models.IntegerField(default=0)),
                ('sphtml', models.IntegerField(default=0)),
                ('spqa', models.IntegerField(default=0)),
                ('djava', models.IntegerField(default=0)),
                ('dphp', models.IntegerField(default=0)),
                ('dhtml', models.IntegerField(default=0)),
                ('dqa', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
