from django.contrib import admin
from arc.models.register_mod import register
from arc.models.prod_mod import product
from arc.models.story_mod import story
from arc.models.prg_mod import prg
from arc.models.project_mod import project
# Register your models here.
admin.site.register(register)
admin.site.register(story)
admin.site.register(product)
admin.site.register(prg)
admin.site.register(project)
