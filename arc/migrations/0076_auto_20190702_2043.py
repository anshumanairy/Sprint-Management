# Generated by Django 2.1.7 on 2019-07-02 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0075_story_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='status',
            field=models.CharField(choices=[('Live', 'Live'), ('ip', 'In Progress'), ('hd', 'HTML DONE'), ('ad', 'API DONE'), ('qa', 'QA'), ('pd', 'Pending Development'), ('bl', 'Blocked'), ('ba', 'Blocked on API'), ('bh', 'Blocked on HTML'), ('bm', 'Blocked on Mock'), ('bs', 'Blocked on Spec'), ('nn', 'Not Needed'), ('ns', 'Next Sprint'), ('dup', 'Duplicate'), ('cr', 'CR')], default='Live', max_length=10),
        ),
    ]
