from django import forms
from arc.models.story_mod import story
from django.contrib.auth import login,authenticate,logout,get_user_model

class storyform(forms.ModelForm):
    class Meta:
        model=story
        fields = ['story_name','brief_description','description','jira']
