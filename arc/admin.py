from django.contrib import admin
from arc.models.register_mod import user_detail
from arc.models.prod_mod import sprint
from arc.models.story_mod import story
from arc.models.story_details_mod import story_details
from arc.models.prg_mod import progress
from arc.models.project_mod import project
from arc.models.comments_mod import comments
from arc.models.reg_mod import user_sprint_detail
from arc.models.project_details_mod import project_details
from arc.models.profile_mod import display_picture
from django.contrib.auth.models import Permission
from django.contrib import admin

admin.site.register(Permission)
admin.site.register(user_detail)
admin.site.register(display_picture)
admin.site.register(story)
admin.site.register(story_details)
admin.site.register(sprint)
admin.site.register(progress)
admin.site.register(project)
admin.site.register(comments)
admin.site.register(project_details)
admin.site.register(user_sprint_detail)
