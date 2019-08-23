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
def view_story(request):
    try:
        id = request.session['id']
        pid2 = request.session['pid']
    except Exception as ex:
        messages.info(request, 'Session expired for this ID! Please login again!')
        return(redirect('login'))
    if id==0 or pid2==0:
        messages.info(request, 'Select a valid sprint and project first!')
        return redirect('product')
    permission=[]
    per1 = Permission.objects.filter(group__user=request.user)
    pic=''
    if display_picture.objects.filter(idx = request.user.id).exists()==True:
        pic = display_picture.objects.get(idx = request.user.id)
    else:
        pass
    for i in per1:
        permission.append(i.name)
    if request.user.has_perm("view_stories.view_stories") or ("view_stories") in permission:
        data1 = sprint.objects.filter(project_id=pid2)
        n = project.objects.all().exclude(id=0)
        if project.objects.filter(id=pid2).exists()==True:
            nx = project.objects.get(id=pid2)
        else:
            messages.info(request, 'Select a valid sprint and project first!')
            return redirect('product')
        nx1 = sprint.objects.get(id = id).name
        data = story_details.objects.filter(sprint_id=id)

        #progress part
        datax = user_sprint_detail.objects.filter(roles='dev',sprint_id=id)
        list2x={}
        list3x={}
        list4x={}
        list5x={}
        list6x={}
        list7x={}
        list8x={}
        list9x={}
        ny=-1
        py=-1
        hy=-1
        qy=-1
        for i1 in data:
            ny+=1
            i3 = story.objects.get(id=i1.story_id)
            if i1.dev_java not in ['',None]:
                list2x[i3.jira]={}
                list3x[i3.jira]={}
                if progress.objects.filter(story_id=id,dev_name=i1.dev_java,jira_id=i3.jira).exists()==True:
                    st1 = progress.objects.filter(story_id=id,dev_name=i1.dev_java,jira_id=i3.jira)
                    list2x[i3.jira][ny]={}
                    list3x[i3.jira][ny]={}
                    xy=0
                    for i2 in st1:
                        list2x[i3.jira][ny][str(xy)]=str(i2.work_date)
                        list3x[i3.jira][ny][str(xy)]=i2.status
                        xy+=1

            py+=1
            if i1.dev_php not in ['',None]:
                list4x[i3.jira]={}
                list5x[i3.jira]={}
                if progress.objects.filter(story_id=id,dev_name=i1.dev_php,jira_id=i3.jira).exists()==True:
                    st1 = progress.objects.filter(story_id=id,dev_name=i1.dev_php,jira_id=i3.jira)
                    list4x[i3.jira][py]={}
                    list5x[i3.jira][py]={}
                    xy=0
                    for i2 in st1:
                        list4x[i3.jira][py][str(xy)]=str(i2.work_date)
                        list5x[i3.jira][py][str(xy)]=i2.status
                        xy+=1

            hy+=1
            if i1.dev_html not in ['',None]:
                list6x[i3.jira]={}
                list7x[i3.jira]={}
                if progress.objects.filter(story_id=id,dev_name=i1.dev_html,jira_id=i3.jira).exists()==True:
                    st1 = progress.objects.filter(story_id=id,dev_name=i1.dev_html,jira_id=i3.jira)
                    list6x[i3.jira][hy]={}
                    list7x[i3.jira][hy]={}
                    xy=0
                    for i2 in st1:
                        list6x[i3.jira][hy][str(xy)]=str(i2.work_date)
                        list7x[i3.jira][hy][str(xy)]=i2.status
                        xy+=1

            qy+=1
            if i1.dev_qa not in ['',None]:
                list8x[i3.jira]={}
                list9x[i3.jira]={}
                if progress.objects.filter(story_id=id,dev_name=i1.dev_qa,jira_id=i3.jira).exists()==True:
                    st1 = progress.objects.filter(story_id=id,dev_name=i1.dev_qa,jira_id=i3.jira)
                    list8x[i3.jira][qy]={}
                    list9x[i3.jira][qy]={}
                    xy=0
                    for i2 in st1:
                        list8x[i3.jira][qy][str(xy)]=str(i2.work_date)
                        list9x[i3.jira][qy][str(xy)]=i2.status
                        xy+=1

        jd1x=json.dumps(list2x)
        jd2x=json.dumps(list3x)
        jd3x=json.dumps(list4x)
        jd4x=json.dumps(list5x)
        jd5x=json.dumps(list6x)
        jd6x=json.dumps(list7x)
        jd7x=json.dumps(list8x)
        jd8x=json.dumps(list9x)

        px = sprint.objects.get(id=id)
        xx = px.sprint_start_date
        yy = px.sprint_dev_end_date
        xx=str(xx)
        aa,bb,cc = xx.split('-')
        yy=str(yy)
        dd,ee,ff = yy.split('-')
        aa=int(aa)
        bb=int(bb)
        cc=int(cc)
        dd=int(dd)
        ee=int(ee)
        ff=int(ff)


        # allocation part
        dashboard = story.objects.filter(sprint_id=id)
        dashboard1 = story_details.objects.filter(sprint_id=id)
        d1 = user_sprint_detail.objects.filter(roles='dev',sprint_id=id)
        d2 = user_sprint_detail.objects.filter(roles='dev',java='True',sprint_id=id)
        d3 = user_sprint_detail.objects.filter(roles='dev',php='True',sprint_id=id)
        d4 = user_sprint_detail.objects.filter(roles='dev',html='True',sprint_id=id)
        d5 = user_sprint_detail.objects.filter(roles='dev',qa='True',sprint_id=id)
        sjava = user_sprint_detail.objects.aggregate(Sum('story_points_java'))['story_points_java__sum']
        sphp = user_sprint_detail.objects.aggregate(Sum('story_points_php'))['story_points_php__sum']
        shtml = user_sprint_detail.objects.aggregate(Sum('story_points_html'))['story_points_html__sum']
        sqa = user_sprint_detail.objects.aggregate(Sum('story_points_qa'))['story_points_qa__sum']
        list11=[]
        for i in d1:
            j = story_details.objects.filter(sprint_id=id, dev_java=i.name)
            if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                list11.append(0)
            else:
                list11.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
        a=sum(list11)

        list21=[]
        for i in d1:
            j = story_details.objects.filter(sprint_id=id, dev_php=i.name)
            if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                list21.append(0)
            else:
                list21.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
        b=sum(list21)

        list31=[]
        for i in d1:
            j = story_details.objects.filter(sprint_id=id, dev_html=i.name)
            if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                list31.append(0)
            else:
                list31.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
        c=sum(list31)

        list41=[]
        for i in d1:
            j = story_details.objects.filter(sprint_id=id, dev_qa=i.name)
            if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                list41.append(0)
            else:
                list41.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
        d=sum(list41)

        form = storyform(request.POST or None)
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        datay = story.objects.filter(sprint_id=id)
        for i in datay:
            list1.append(i.id)
            list2.append(i.story_name)
            list3.append(i.description)
            list4.append(i.jira)
        jd1=json.dumps(list1)
        jd2=json.dumps(list2)
        jd3=json.dumps(list3)
        jd4=json.dumps(list4)
        name=request.user.username
        if request.method=='GET':
            if 'red' in request.GET:
                idx = request.GET.get('red')
                request.session['story_id'] = idx
                return(redirect('story'))

            if 'delete_story' in request.GET:
                x = request.GET.get('delete_story')
                if request.user.has_perm("delete_story.delete_story") or ("delete_story") in permission:
                    story.objects.filter(sprint_id=id,id=x).delete()
                    story_details.objects.filter(sprint_id=id,story_id=x).delete()
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('view_story')
                return(redirect('view_story'))
                # print(x)
            if 's_name' in request.GET:
                sn = request.GET.get('s_name')
                sd = request.GET.get('desc')
                soj = request.GET.get('old_jira')
                snj = request.GET.get('new_jira')
                p = story.objects.filter(sprint_id=id,jira=soj).latest('id')
                p.story_name = sn
                p.description = sd
                p.jira = snj
                p1 = story_details.objects.filter(story_id=p.id).latest('id')
                p1.jira=snj
                if request.user.has_perm("edit_story.edit_story") or ("edit_story") in permission:
                    p.save()
                    p1.save()
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('view_story')
                return(redirect('view_story'))

            if 'assign_data' in request.GET:
                if request.user.has_perm("allocate_points.allocate_points") or ("allocate_points") in permission:
                    java_dev = request.GET.get('java_sel')
                    p1 = request.GET.get('points1')
                    idy = request.GET.get('idx')
                    dt = datetime.date.today()
                    if int(p1)>0:
                        px = story.objects.get(sprint_id=id,id=idy)
                        p = story_details.objects.get(story_id=px.id)
                        dev1 = p.dev_java
                        p.dev_java = java_dev
                        p.assigned_java_points = int(p1)
                        p.java_points_left = int(p1)
                        p.save()
                        list1=[]
                        q = story.objects.get(id=px.id)
                        for i in d1:
                            j = story_details.objects.filter(sprint_id=id, dev_java=i.name)
                            if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                                list1.append(0)
                            else:
                                list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                                if q.overall_status in [None,'',' ']:
                                    q.overall_status='Live'
                                    q.save()
                                    pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=java_dev,work_date=dt.strftime("%Y-%m-%d"))
                                    pr2.save()
                                p.save()
                        a=sum(list1)

                        # user change
                        if dev1 != java_dev and dev1 not in [' ','',None] :
                            creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                            creg1 = user_sprint_detail.objects.get(name=java_dev,sprint_id=id)
                            j = story_details.objects.filter(sprint_id=id, dev_java=dev1)
                            j1 = story_details.objects.filter(sprint_id=id, dev_java=java_dev)

                            if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                                creg.delta_java = creg.story_points_java
                            else:
                                creg.delta_java = creg.story_points_java - (j1.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])

                            if j1.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                                creg1.delta_java = creg1.story_points_java
                            else:
                                creg1.delta_java = creg1.story_points_java - (j1.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])

                            creg.save()
                            creg1.save()

                            # pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).latest('id')
                            # pr1 = progress(story_id=id,jira_id=pr.jira_id,dev_name=java_dev,actual = pr.actual,left=pr.left,calculated_left=pr.left)
                            # pr1.save()
                            # pr = story_details.objects.filter(sprint_id=id,jira=).latest('id')
                            dt = datetime.date.today()
                            if progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).exists():
                                pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).latest('id')
                                pr1 = progress(story_id=px.id,jira_id=px.jira,dev_name=java_dev,actual = pr.actual,left=pr.left,calculated_left=pr.left,work_date=dt.strftime("%Y-%m-%d"))
                                pr1.save()
                            else:
                                pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=java_dev,work_date=dt.strftime("%Y-%m-%d"))
                                pr2.save()


                if 'php_sel' in request.GET:
                    php_dev = request.GET.get('php_sel')
                    p2 = request.GET.get('points2')
                    idy = request.GET.get('idx')
                    if int(p2)>0:
                        p1 = story.objects.get(sprint_id=id,id=idy)
                        p = story_details.objects.get(story_id=p1.id)
                        q = story.objects.get(id=p1.id)
                        dev1 = p.dev_php
                        # n = user_sprint_detail.objects.get(name=php_dev,sprint_id=id1)
                        p.dev_php = php_dev
                        p.assigned_php_points = int(p2)
                        p.php_points_left = int(p2)
                        p.save()
                        list2=[]
                        for i in d1:
                            # j1 = story.objects.filter(sprint_id=id, dev_php=i.name)
                            j = story_details.objects.filter(sprint_id=id, dev_php=i.name)
                            if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                                list2.append(0)
                            else:
                                list2.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                                if q.overall_status in [None,'',' ']:
                                    q.overall_status='Live'
                                    q.save()
                                    pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=php_dev,work_date=dt.strftime("%Y-%m-%d"))
                                    pr2.save()
                                p.save()
                        b=sum(list2)

                        if dev1 != None and dev1 != php_dev :
                            creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                            creg1 = user_sprint_detail.objects.get(name=php_dev,sprint_id=id)
                            j = story_details.objects.filter(sprint_id=id, dev_php=dev1)
                            j1 = story_details.objects.filter(sprint_id=id, dev_php=php_dev)

                            if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                                creg.delta_php = creg.story_points_php
                            else:
                                creg.delta_php = creg.story_points_php - (j1.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])

                            if j1.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                                creg1.delta_php = creg1.story_points_php
                            else:
                                creg1.delta_php = creg1.story_points_php - (j1.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])

                            creg.save()
                            creg1.save()

                            # pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira)
                            # for p1 in pr:
                            #     p1.dev_name = php_dev
                            #     p1.save()
                            dt = datetime.date.today()
                            if progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).exists():
                                pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).latest('id')
                                pr1 = progress(story_id=px.id,jira_id=px.jira,dev_name=php_dev,actual = pr.actual,left=pr.left,calculated_left=pr.left,work_date=dt.strftime("%Y-%m-%d"))
                                pr1.save()
                            else:
                                pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=php_dev,work_date=dt.strftime("%Y-%m-%d"))
                                pr2.save()

                if 'html_sel' in request.GET:
                    html_dev = request.GET.get('html_sel')
                    p3 = request.GET.get('points3')
                    idy = request.GET.get('idx')
                    if int(p3)>0:
                        # n = user_sprint_detail.objects.get(name=html_dev,sprint_id=id1)
                        p1 = story.objects.get(sprint_id=id,id=idy)
                        p = story_details.objects.get(story_id=p1.id)
                        q = story.objects.get(id=p1.id)
                        dev1 = p.dev_html
                        p.dev_html = html_dev
                        p.assigned_html_points = int(p3)
                        p.html_points_left = int(p3)
                        p.save()
                        list3=[]
                        for i in d1:
                            j = story_details.objects.filter(sprint_id=id, dev_html=i.name)
                            if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                                list3.append(0)
                            else:
                                list3.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                                if q.overall_status in [None,'',' ']:
                                    q.overall_status='Live'
                                    q.save()
                                    pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=html_dev,work_date=dt.strftime("%Y-%m-%d"))
                                    pr2.save()
                                p.save()
                        c=sum(list3)

                        # user change
                        if dev1 != None and dev1 != html_dev :
                            creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                            creg1 = user_sprint_detail.objects.get(name=html_dev,sprint_id=id)
                            j = story_details.objects.filter(sprint_id=id, dev_html=dev1)
                            j1 = story_details.objects.filter(sprint_id=id, dev_html=html_dev)

                            if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                                creg.delta_html = creg.story_points_html
                            else:
                                creg.delta_html = creg.story_points_html - (j1.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])

                            if j1.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                                creg1.delta_html = creg1.story_points_html
                            else:
                                creg1.delta_html = creg1.story_points_html - (j1.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])

                            creg.save()
                            creg1.save()

                            # pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira)
                            # for p1 in pr:
                            #     p1.dev_name = html_dev
                            #     p1.save()
                            dt = datetime.date.today()
                            if progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).exists():
                                pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).latest('id')
                                pr1 = progress(story_id=px.id,jira_id=px.jira,dev_name=html_dev,actual = pr.actual,left=pr.left,calculated_left=pr.left,work_date=dt.strftime("%Y-%m-%d"))
                                pr1.save()
                            else:
                                pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=html_dev,work_date=dt.strftime("%Y-%m-%d"))
                                pr2.save()

                if 'qa_sel' in request.GET:
                    qa_dev = request.GET.get('qa_sel')
                    p4 = request.GET.get('points4')
                    idy = request.GET.get('idx')
                    if int(p4)>0:
                        # n = user_sprint_detail.objects.get(name=qa_dev,sprint_id=id1)
                        p1 = story.objects.get(sprint_id=id,id=idy)
                        p = story_details.objects.get(story_id=p1.id)
                        q = story.objects.get(id=p1.id)
                        dev1 = p.dev_qa
                        p.dev_qa = qa_dev
                        p.assigned_qa_points = int(p4)
                        p.qa_points_left = int(p4)
                        p.save()
                        list4=[]
                        for i in d1:
                            j = story_details.objects.filter(sprint_id=id, dev_qa=i.name)
                            if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                                list4.append(0)
                            else:
                                list4.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                                if q.overall_status in [None,'',' ']:
                                    q.overall_status='Live'
                                    q.save()
                                    pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=qa_dev,work_date=dt.strftime("%Y-%m-%d"))
                                    pr2.save()
                                p.save()
                        d=sum(list4)

                        # user change
                        if dev1 != None and dev1 != qa_dev :
                            creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                            creg1 = user_sprint_detail.objects.get(name=qa_dev,sprint_id=id)
                            j = story_details.objects.filter(sprint_id=id, dev_qa=dev1)
                            j1 = story_details.objects.filter(sprint_id=id, dev_qa=qa_dev)

                            if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                                creg.delta_qa = creg.story_points_qa
                            else:
                                creg.delta_qa = creg.story_points_qa - (j1.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])

                            if j1.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                                creg1.delta_qa = creg1.story_points_qa
                            else:
                                creg1.delta_qa = creg1.story_points_qa - (j1.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])

                            creg.save()
                            creg1.save()

                            # pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira)
                            # for p1 in pr:
                            #     p1.dev_name = qa_dev
                            #     p1.save()
                            dt = datetime.date.today()
                            if progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).exists():
                                pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira).latest('id')
                                pr1 = progress(story_id=px.id,jira_id=px.jira,dev_name=qa_dev,actual = pr.actual,left=pr.left,calculated_left=pr.left,work_date=dt.strftime("%Y-%m-%d"))
                                pr1.save()
                            else:
                                pr2 = progress(story_id=px.id,jira_id=px.jira,dev_name=qa_dev,work_date=dt.strftime("%Y-%m-%d"))
                                pr2.save()

                    return(redirect('view_story'))

                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return(redirect('view_story'))

        if request.method=='POST':
            if 'select_sprint' in request.POST:
                select = request.POST.get('select_sprint')
                for i in data1:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                return redirect('view_story')

            if 'select_project' in request.POST:
                name1 = request.POST.get('select_project')
                proid = project.objects.get(name=name1).id
                request.session['pid'] = proid
                spr = sprint.objects.filter(project_id=proid).first()
                request.session['id'] = spr.id
                return redirect('view_story')

            if 'csv_button' in request.POST:
                csv_file = request.FILES['file1']
                if not csv_file.name.endswith('.csv'):
                    messages.info(request, 'Please choose a CSV File!')
                    return redirect('view_story')
                data_set = csv_file.read().decode('UTF-8')
                lines = data_set.split("\n")
                firstline = True
                try:
                    for line in lines:
                        if firstline == True:
                            firstline = False
                            continue
                        else:
                            fields = line.split(",")
                            stx = story.objects.filter(sprint_id=id)
                            l=0
                            for i in stx:
                                if fields[2]==i.jira:
                                    l+=1
                            if l==0:
                                k=0
                                for i3 in user_detail.objects.all():
                                    if fields[3]==i3.name:
                                        k+=1
                                    if fields[5]==i3.name:
                                        k+=1
                                    if fields[7]==i3.name:
                                        k+=1
                                    if fields[9]==i3.name:
                                        k+=1
                                if fields[3]=='':
                                    k+=1
                                if fields[5]=='':
                                    k+=1
                                if fields[7]=='':
                                    k+=1
                                if fields[9]=='':
                                    k+=1
                                if fields[10] in ['Complete','Live','In Progress','HTML Done','PHP Done','API Done','QA','Pending Deployment','Blocked','Blocked on API','Blocked on HTML','Blocked on Mock','Blocked on Spec','Not Needed','Next Sprint','Duplicate','CR','',' ']:
                                    k+=1
                                if k==5:
                                    for i2 in range(4,11,2):
                                        if fields[i2] in ['null', 'None', '','None ',' ']:
                                            fields[i2] = 0
                                        if int(fields[i2])<0:
                                            fields[i2] = 0
                                    z1 = story(sprint_id=id,story_name=fields[0],description=fields[1],jira=fields[2])
                                    if request.user.has_perm("add_story.add_story") or ("add_story") in permission:
                                        z1.save()
                                    else:
                                        messages.info(request, 'UNAUTHORIZED!')
                                        return redirect('view_story')
                                    z2 = story.objects.filter(sprint_id=id,story_name=fields[0],description=fields[1],jira=fields[2],overall_status=fields[11]).latest('id')
                                    dt = datetime.date.today()
                                    z3 = story_details(sprint_id=id,jira=fields[2],story_id=z2.id,dev_java=fields[3],assigned_java_points=int(fields[4]),dev_php=fields[5],assigned_php_points=int(fields[6]),dev_html=fields[7],assigned_html_points=int(fields[8]),dev_qa=fields[9],assigned_qa_points=int(fields[10]))
                                    dt = datetime.date.today()
                                    if request.user.has_perm("add_story.add_story") or ("add_story") in permission:
                                        # check developer skillwise check 4 times using if conditions
                                        if fields[3] not in ['',' ',None]:
                                            pr2 = progress(story_id=z2.id,jira_id=fields[2],dev_name=fields[3],work_date=dt.strftime("%Y-%m-%d"))
                                            pr2.save()
                                        if fields[5] not in ['',' ',None]:
                                            pr2 = progress(story_id=z2.id,jira_id=fields[2],dev_name=fields[5],work_date=dt.strftime("%Y-%m-%d"))
                                            pr2.save()
                                        if fields[7] not in ['',' ',None]:
                                            pr2 = progress(story_id=z2.id,jira_id=fields[2],dev_name=fields[7],work_date=dt.strftime("%Y-%m-%d"))
                                            pr2.save()
                                        if fields[9] not in ['',' ',None]:
                                            pr2 = progress(story_id=z2.id,jira_id=fields[2],dev_name=fields[9],work_date=dt.strftime("%Y-%m-%d"))
                                            pr2.save()
                                        z3.save()
                                    else:
                                        messages.info(request, 'UNAUTHORIZED!')
                                        return redirect('view_story')
                except:
                    pass
                return(redirect('view_story'))

            if 'spr1' in request.POST:
                form = storyform(request.POST)
                if form.is_valid():
                    form.instance.sprint_id=id
                    p = story.objects.all()
                    # for i in p:
                    #     if form.instance.jira == i.jira:
                    #         messages.info(request, 'Jira ID already exists. Please choose another one!')
                    #         return redirect('view_story')
                    form.save()
                    z4 = story.objects.latest('id')
                    dt = datetime.date.today()
                    z5 = story_details(sprint_id=id,story_id=z4.id,jira=z4.jira)
                    if request.user.has_perm("add_story.add_story") or ("add_story") in permission:
                        z5.save()
                    else:
                        messages.info(request, 'UNAUTHORIZED!')
                        return redirect('view_story')
                    return redirect('view_story')
                else:
                    messages.info(request, 'Data Not Stored!')
                    return redirect('view_story')
            else:
                form = storyform()

        return render(request,'view_story.html',{'permission':permission,'datay':datay,'jd8x':jd8x,'jd7x':jd7x,'jd6x':jd6x,'jd5x':jd5x,'jd4x':jd4x,'jd3x':jd3x,'aa':aa,'bb':bb,'cc':cc,'dd':dd,'ee':ee,'ff':ff,'jd1x':jd1x,'jd2x':jd2x,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'dashboard':dashboard,'list11':list11,'list21':list21,'list31':list31,'list41':list41,'a':a,'b':b,'c':c,'d':d,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'d1':d1,'form':form,'data':data,'jd1':jd1,'jd2':jd2,'jd3':jd3,'jd4':jd4,'n':n,'nx':nx,'data1':data1,'nx1':nx1,'name':name,'dashboard1':dashboard1,'pic':pic})
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')
