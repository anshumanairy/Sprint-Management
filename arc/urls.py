from django.urls import path
from arc.controller import views
from django.conf.urls import url,include

urlpatterns = [
    url(r'^$',views.reg,name="register"),
    # url(r'^quikr/',views.quikr,name="quikr"),
    url(r'^login/',views.log,name="login"),
    url(r'^profile/',views.profile,name="profile"),
    url(r'^product/',views.prod,name="product"),
    url(r'^view_story/',views.view_story,name="view_story"),
    url(r'^blog/',views.blog,name="blog"),
    url(r'^progress/',views.qaprg,name="qaprg"),
    url(r'^bandwidth/',views.bandwidth,name="bandwidth"),
    url(r'^tasks/',views.tasks,name="tasks"),
    url(r'^logout/$' , views.user_logout , name='logout'),
]
