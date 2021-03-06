# Generated by Django 2.2 on 2019-08-14 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arc', '0074_remove_story_details_ostatus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='abhtml',
            new_name='available_bandwidth_html',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='abjava',
            new_name='available_bandwidth_java',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='abphp',
            new_name='available_bandwidth_php',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='abqa',
            new_name='available_bandwidth_qa',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='dhtml',
            new_name='delta_html',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='djava',
            new_name='delta_java',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='dphp',
            new_name='delta_php',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='dqa',
            new_name='delta_qa',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='planned',
            new_name='planned_leaves',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='sphtml',
            new_name='story_points_html',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='spjava',
            new_name='story_points_java',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='spphp',
            new_name='story_points_php',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='spqa',
            new_name='story_points_qa',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='unplanned',
            new_name='unplanned_leaves',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='vfhtml',
            new_name='velocity_factor_html',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='vfjava',
            new_name='velocity_factor_java',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='vfqa',
            new_name='velocity_factor_php',
        ),
        migrations.RenameField(
            model_name='user_sprint_detail',
            old_name='vfphp',
            new_name='velocity_factor_qa',
        ),
    ]
