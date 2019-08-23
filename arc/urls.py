from django.urls import path
from arc.controller import register
from arc.controller import product
from arc.controller import bandwidth
from arc.controller import progress
from arc.controller import detail_story
from arc.controller import stories
from arc.controller import report
from arc.controller import profile
from arc.controller import admin
from django.conf.urls import url,include

urlpatterns = [
    url(r'^$',register.reg,name="register"),
    url(r'^login/',register.log,name="login"),
    url(r'^logout/$' , register.user_logout , name='logout'),
    url(r'^product/',product.prod,name="product"),
    url(r'^view_story/',stories.view_story,name="view_story"),
    url(r'^story/',detail_story.blog,name="story"),
    url(r'^progress/',progress.qaprg,name="qaprg"),
    url(r'^bandwidth/',bandwidth.bandwidth,name="bandwidth"),
    url(r'^tasks/',report.tasks,name="tasks"),
    url(r'^profile/',profile.profile,name="profile"),
    url(r'^admin/',admin.admin,name="admin"),
]
