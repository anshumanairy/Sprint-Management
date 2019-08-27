from django.shortcuts import render,redirect
from arc.forms.register_forms import registerform,UserForm
from arc.forms.prod_forms import sprintform
from arc.forms.story_forms import storyform
from arc.models.register_mod import user_detail
from arc.models.project_mod import project
from arc.models.story_mod import story
from arc.models.story_details_mod import story_details
from arc.models.project_details_mod import project_details
from arc.models.prod_mod import sprint
from arc.models.comments_mod import comments
from arc.models.prg_mod import progress
from arc.models.profile_mod import display_picture
from arc.models.reg_mod import user_sprint_detail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.template.response import TemplateResponse
from datetime import timedelta
from django.db.models import Sum
import datetime
import numpy as np
import json
import csv, io
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import requests
from Crypto.Cipher import AES
import base64
import hashlib
import hmac
import jwt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.utils.timezone import utc
from django.utils import timezone

@login_required(login_url='/')
def blog(request):
    try:
        id1 = request.session['id']
        pid2 = request.session['pid']
    except Exception as ex:
        messages.info(request, 'Session expired for this ID! Please login again!')
        return(redirect('login'))
    if id1==0 or pid2==0:
        messages.info(request, 'Select a valid sprint and project first!')
        return redirect('product')
    permission=[]
    pic=''
    if display_picture.objects.filter(idx = request.user.id).exists()==True:
        pic = display_picture.objects.get(idx = request.user.id)
    else:
        pass
    per1 = Permission.objects.filter(group__user=request.user)
    for i in per1:
        permission.append(i.name)
    if request.user.has_perm("view_detail_story.view_detail_story") or ("view_detail_story") in permission:
        data1 = sprint.objects.filter(project_id=pid2)
        sid = request.session['story_id']
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = sprint.objects.get(id = id1).name
        name = request.user.username
        st = story_details.objects.filter(sprint_id=id1,story_id=sid)
        stz = story.objects.get(sprint_id=id1,id=sid)

        # for tabular history
        history=[]
        h=0
        dev=''
        update = progress.objects.filter(story_id=sid,jira_id=stz.jira).order_by('work_date')
        for up in update:
            history.append([])
            dt = up.work_date
            history[h].append(dt.strftime("%Y-%m-%d"))
            history[h].append(up.dev_name)
            if up.actual==0.5:
                history[h].append('Quarter Day')
                history[h].append(up.status)
            elif up.actual==1.0:
                history[h].append('Half Day')
                history[h].append(up.status)
            elif up.actual==1.5:
                history[h].append('Three Quarters Day')
                history[h].append(up.status)
            elif up.actual==2.0:
                history[h].append('Full Day')
                history[h].append(up.status)
            elif dev != up.dev_name:
                dev = up.dev_name
                history[h].append('')
                history[h].append('Developer Changed')
            h+=1
        picture=[]
        comm={}
        n=0
        story_comments = comments.objects.filter(story_id=sid)
        comm[n]={}
        for j in story_comments:
            name1 = User.objects.get(id=j.user_id)
            comm[n][j.time_of_comment]={}
            comm[n][j.time_of_comment][j.comment]=name1.username
            reg1 = display_picture.objects.get(idx = name1.id).profile_picture
            picture.append(reg1)
        n+=1

        if request.method=='POST':
            if 'select_project' in request.POST:
                name1 = request.POST.get('select_project')
                proid = project.objects.get(name=name1).id
                request.session['pid'] = proid
                spr = sprint.objects.filter(project_id=proid).first()
                request.session['id'] = spr.id
                return redirect('story')

            if 'select_sprint' in request.POST:
                select = request.POST.get('select_sprint')
                for i in data1:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                return redirect('story')

        if request.method=='GET':
            if 'time' in request.GET:
                developer = request.GET.get('developer')
                time = request.GET.get('time')
                print(developer)
                print(time)
                id_of_user = User.objects.get(username=developer)
                comms = comments.objects.get(user_id=id_of_user.id,time_of_comment=time)
                # comms.delete()
                return redirect('story')

            if 'brief_desc' in request.GET:
                desc = request.GET.get('brief_desc')
                change = story.objects.get(id=sid)
                change.brief_description=desc
                change.save()
                return redirect('story')

            if 'comment_holder' in request.GET:
                comment_received=request.GET.get('comment_holder')
                id1 = request.GET.get('sid')
                date_comm = timezone.localtime(timezone.now()).strftime("%a %b %d, %Y")
                time_comm = timezone.localtime(timezone.now()).strftime("%H:%M:%S")
                final_time= time_comm+" on "+date_comm
                comm = comments(story_id=sid,comment=comment_received,user_id=request.user.id,time_of_comment=final_time)
                comm.save()
                return redirect('story')

        return render(request,'blog.html/',{'picture':picture,'pic':pic,'stz':stz,'permission':permission,'history':history,'name':name,'comm':comm,'st':st,'n0':n0,'nx':nx,'nx1':nx1,'data1':data1})
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')
