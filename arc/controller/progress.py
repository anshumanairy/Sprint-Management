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
def qaprg(request):
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
    if request.user.is_superuser or (user_sprint_detail.objects.filter(uname=request.user.username,sprint_id=id1,roles='man').exists()==True):
        data1 = sprint.objects.filter(project_id=pid2)
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = sprint.objects.get(id = id1).name
        data = user_sprint_detail.objects.filter(roles='dev',sprint_id=id1)
        list1=[]
        j=0
        p = sprint.objects.get(id=id1)
        x = p.sprint_start_date
        y = p.sprint_dev_end_date
        x=str(x)
        a,b,c = x.split('-')
        y=str(y)
        d,e,f = y.split('-')
        a=int(a)
        b=int(b)
        c=int(c)
        d=int(d)
        e=int(e)
        f=int(f)
        list2={}
        n=0
        for i1 in data:
            st1 = story_details.objects.filter(sprint_id=id1,dev_java=i1.name) | story_details.objects.filter(sprint_id=id1,dev_php=i1.name) | story_details.objects.filter(sprint_id=id1,dev_html=i1.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i1.name)
            list2[i1.name]={}
            for j11 in st1:
                j1 = story.objects.get(sprint_id=id1,id=j11.story_id)
                if progress.objects.filter(story_id=j1.id,jira_id=j1.jira,dev_name=i1.name).exists()==True:
                    p1 = progress.objects.filter(story_id=j1.id,jira_id=j1.jira,dev_name=i1.name).order_by('-id')
                    list2[i1.name][n]={}
                    for k1 in p1:
                        list2[i1.name][n][str(k1.work_date)]=str(k1.work_date)
                    n+=1
                else:
                    n+=1
        jd1=json.dumps(list2)

        list3={}
        n=0
        for i2 in data:
            st1 = story_details.objects.filter(sprint_id=id1,dev_java=i2.name) | story_details.objects.filter(sprint_id=id1,dev_php=i2.name) | story_details.objects.filter(sprint_id=id1,dev_html=i2.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i2.name)
            list3[i2.name]={}
            for j22 in st1:
                j2 = story.objects.get(sprint_id=id1,id=j22.story_id)
                if progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                    r=0
                    p1 = progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
                    list3[i2.name][n]={}
                    for k2 in p1:
                        list3[i2.name][n][str(r)]=k2.status
                        r+=1
                        # print(k2.status)
                    n+=1
                else:
                    n+=1
        jd2=json.dumps(list3)
        # print(list3)

        list4={}
        n=0
        for i2 in data:
            st1 = story_details.objects.filter(sprint_id=id1,dev_java=i2.name) | story_details.objects.filter(sprint_id=id1,dev_php=i2.name) | story_details.objects.filter(sprint_id=id1,dev_html=i2.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i2.name)
            list4[i2.name]={}
            for j22 in st1:
                j2 = story.objects.get(sprint_id=id1,id=j22.story_id)
                if progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                    p1 = progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
                    for k2 in p1:
                        list4[i2.name][n]=k2.jira_id
                        n+=1
                else:
                    n+=1
        jd3=json.dumps(list4)

        count=0
        for i in data:
            list1.append([])
            k=0
            st = story_details.objects.filter(sprint_id=id1,dev_java=i.name) | story_details.objects.filter(sprint_id=id1,dev_php=i.name) | story_details.objects.filter(sprint_id=id1,dev_html=i.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i.name)
            for r1 in st:
                r = story.objects.get(sprint_id=id1,id=r1.story_id)
                list1[j].append([])
                list1[j][k].append(r.story_name)
                list1[j][k].append(r.jira)
                if r1.dev_java==i.name:
                    list1[j][k].append(r1.assigned_java_points)
                    list1[j][k].append(r.overall_status)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r1.java_points_done)
                    list1[j][k].append(float(r1.assigned_java_points)-r1.java_points_done)
                    if progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_java).exclude(status='').exists()==True:
                        z1 = progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_java).exclude(status='').latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r1.assigned_java_points)-r1.java_points_done)
                    list1[j][k].append(r.id)
                elif r1.dev_php==i.name:
                    list1[j][k].append(r1.assigned_php_points)
                    list1[j][k].append(r.overall_status)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r1.php_points_done)
                    list1[j][k].append(float(r1.assigned_php_points)-r1.php_points_done)
                    if progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_php).exclude(status='').exists()==True:
                        z1 = progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_php).exclude(status='').latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r1.assigned_php_points)-r1.php_points_done)
                    list1[j][k].append(r.id)
                elif r1.dev_html==i.name:
                    list1[j][k].append(r1.assigned_html_points)
                    list1[j][k].append(r.overall_status)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r1.html_points_done)
                    list1[j][k].append(float(r1.assigned_html_points)-r1.html_points_done)
                    if progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_html).exclude(status='').exists()==True:
                        z1 = progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_html).exclude(status='').latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r.assigned_html_points)-r.html_points_done)
                    list1[j][k].append(r.id)
                elif r1.dev_qa==i.name:
                    list1[j][k].append(r1.assigned_qa_points)
                    list1[j][k].append(r.overall_status)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r1.qa_points_done)
                    list1[j][k].append(float(r1.assigned_qa_points)-r1.qa_points_done)
                    if progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_qa).exclude(status='').exists()==True:
                        z1 = progress.objects.filter(story_id=r.id,jira_id=r.jira,dev_name=r1.dev_qa).exclude(status='').latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r1.assigned_qa_points)-r1.qa_points_done)
                    list1[j][k].append(r.id)

                k+=1
                count=count+1;
            j+=1
        name = request.user.username
        if request.method=='GET':
            if 'red' in request.GET:
                idx = request.GET.get('red')
                request.session['story_id'] = idx
                return(redirect('story'))

            if 'as' in request.GET:
                s = request.GET.get('sel')
                j = request.GET.get('jid')
                n1 = request.GET.get('name1')
                p1 = story.objects.filter(sprint_id=id1,jira = j).latest('id')
                p = story_details.objects.get(sprint_id=id1,story_id=p1.id)
                p1.overall_status=s
                if request.user.has_perm("change_progress.change_progress") or ("change_progress") in permission:
                    p.save()
                    p1.save()
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                return redirect('qaprg')

            if 'bs1' in request.GET:
                if request.user.has_perm("change_progress.change_progress") or ("change_progress") in permission:
                    j = request.GET.get('j1')
                    n2 = request.GET.get('name2')
                    left1 = request.GET.get('left')
                    st = story_details.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                    for ix in st:
                        if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                            pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                            if ix.dev_java==n2:
                                if left1 == (float(ix.assigned_java_points)-ix.java_points_done):
                                    pr1.left= (float(ix.assigned_java_points)-ix.java_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                            elif ix.dev_php==n2:
                                if left1 == (float(ix.assigned_php_points)-ix.php_points_done):
                                    pr1.left= (float(ix.assigned_php_points)-ix.php_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                            elif ix.dev_html==n2:
                                if left1 == (float(ix.assigned_html_points)-ix.html_points_done):
                                    pr1.left= (float(ix.assigned_html_points)-ix.html_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                            else:
                                if left1 == (float(ix.assigned_qa_points)-ix.qa_points_done):
                                    pr1.left= (float(ix.assigned_qa_points)-ix.qa_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                        else:
                            messages.info(request, 'No progress recorded as of yet, cannot change points!')
                            return redirect('qaprg')
                else:
                    messages.info(request, 'UNAUTHORIZED!')

                return redirect('qaprg')

            if 'as1' in request.GET:
                if request.user.has_perm("change_progress.change_progress") or ("change_progress") in permission:
                    stdate = request.GET.get('startdate')
                    prog = request.GET.get('prg')
                    j = request.GET.get('j1')
                    n2 = request.GET.get('name2')
                    frac = request.GET.get('fraction')
                    # left1 = request.GET.get('left')
                    frac1=0
                    if stdate not in [None,'']:
                        if frac=='Quarter Day':
                            frac1=.5
                        elif frac=='Half Day':
                            frac1=1
                        elif frac=='Three Quarters Day':
                            frac1=1.5
                        else:
                            frac1=2
                        st = story_details.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                        cx=0
                        left1 = 0
                        for ix in st:
                            if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                left1 = pr1.left-frac1
                            else:
                                if ix.dev_java==n2:
                                    left1 = (float(ix.assigned_java_points)-ix.java_points_done)-frac1
                                elif ix.dev_php==n2:
                                    left1 = (float(ix.assigned_php_points)-ix.php_points_done)-frac1
                                elif ix.dev_html==n2:
                                    left1 = (float(ix.assigned_html_points)-ix.html_points_done)-frac1
                                else:
                                    left1 = (float(ix.assigned_qa_points)-ix.qa_points_done)-frac1
                            if ix.dev_java==n2:
                                # if pr1.left==(float(ix.assigned_java_points)-ix.java_points_done):
                                #     left1 = (float(ix.assigned_java_points)-(ix.java_points_done))
                                ix.java_points_done = ix.java_points_done + frac1
                                if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                    pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                    cx = pr1.calculated_left - frac1
                                else:
                                    cx = float(ix.assigned_java_points)-frac1
                                ix.java_points_left = cx
                            elif ix.dev_php==n2:
                                # if pr1.left==(float(ix.assigned_php_points)-ix.php_points_done):
                                #     left1 = (float(ix.assigned_php_points)-(ix.php_points_done))
                                ix.php_points_done = ix.php_points_done + frac1
                                # cx=float(ix.assigned_php_points)-float(left1)
                                if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                    pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                    cx = pr1.calculated_left - frac1
                                else:
                                    cx = float(ix.assigned_php_points)-frac1
                                ix.php_points_left = cx
                            elif ix.dev_html==n2:
                                # if pr1.left==(float(ix.assigned_html_points)-ix.html_points_done):
                                #     left1 = (float(ix.assigned_html_points)-(ix.html_points_done))
                                ix.html_points_done = ix.html_points_done + frac1
                                # cx=float(ix.assigned_html_points)-float(left1)
                                if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                    pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                    cx = pr1.calculated_left - frac1
                                else:
                                    cx = float(ix.assigned_html_points)-frac1
                                ix.html_points_left = cx
                            else:
                                # if pr1.left==(float(ix.assigned_qa_points)-ix.qa_points_done):
                                #     left1 = (float(ix.assigned_qa_points)-(ix.qa_points_done))
                                ix.qa_points_done = ix.qa_points_done + frac1
                                # cx=float(ix.assigned_qa_points)-float(left1)
                                if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                    pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                    cx = pr1.calculated_left - frac1
                                else:
                                    cx = float(ix.assigned_qa_points)-frac1
                                ix.qa_points_left = cx
                            ix.save()
                            z = progress(story_id=ix.story_id,jira_id=j,work_date=stdate,status=prog,dev_name=n2,actual=frac1,calculated_left=cx,left=left1)
                            z.save()

                        list2={}
                        for i1 in data:
                            st1 = story_details.objects.filter(sprint_id=id1,dev_java=i1.name) | story_details.objects.filter(sprint_id=id1,dev_php=i1.name) | story_details.objects.filter(sprint_id=id1,dev_html=i1.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i1.name)
                            n=0
                            list2[i1.name]={}
                            for j11 in st1:
                                j1 = story.objects.get(sprint_id=id1,id=j11.story_id)
                                if progress.objects.filter(story_id=ix.story_id,jira_id=j1.jira,dev_name=i1.name).exists()==True:
                                    p1 = progress.objects.filter(story_id=ix.story_id,jira_id=j1.jira,dev_name=i1.name).order_by('-id')
                                    for k1 in p1:
                                        list2[i1.name][n]={}
                                        list2[i1.name][n][str(k1.work_date)]=str(k1.work_date)
                                        n+=1

                        jd1=json.dumps(list2)

                        list3={}
                        m=0
                        for i2 in data:
                            st1 = story_details.objects.filter(sprint_id=id1,dev_java=i2.name) | story_details.objects.filter(sprint_id=id1,dev_php=i2.name) | story_details.objects.filter(sprint_id=id1,dev_html=i2.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i2.name)
                            n=0
                            list3[m]={}
                            for j22 in st1:
                                j2 = story.objects.get(sprint_id=id1,id=j22.story_id)
                                if progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                    p1 = progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
                                    for k2 in p1:
                                        list3[m][n]=k2.status
                                        n+=1
                            m+=1
                        jd2=json.dumps(list3)

                        list4={}
                        m=0
                        for i2 in data:
                            st1 = story_details.objects.filter(sprint_id=id1,dev_java=i2.name) | story_details.objects.filter(sprint_id=id1,dev_php=i2.name) | story_details.objects.filter(sprint_id=id1,dev_html=i2.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i2.name)
                            n=0
                            list4[m]={}
                            for j22 in st1:
                                j2 = story.objects.get(sprint_id=id1,id=j22.story_id)
                                if progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                    p1 = progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
                                    for k2 in p1:
                                        list4[m][n]=k2.jira_id
                                        n+=1
                            m+=1
                        jd3=json.dumps(list4)
                    else:
                        messages.info(request, 'Please select a Valid Date!')
                else:
                    messages.info(request, 'UNAUTHORIZED!')

                return redirect('qaprg')

        if request.method=='POST':
            if 'select_sprint' in request.POST:
                select = request.POST.get('select_sprint')
                for i in data1:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                return redirect('qaprg')

            if 'select_project' in request.POST:
                name1 = request.POST.get('select_project')
                proid = project.objects.get(name=name1).id
                request.session['pid'] = proid
                spr = sprint.objects.filter(project_id=proid).first()
                request.session['id'] = spr.id
                return redirect('qaprg')


    else:

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
        per1 = Permission.objects.filter(group__user=request.user)
        pic=''
        if display_picture.objects.filter(idx = request.user.id).exists()==True:
            pic = display_picture.objects.get(idx = request.user.id)
        else:
            pass
        for i in per1:
            permission.append(i.name)
        name=request.user.username
        data1 = sprint.objects.filter(project_id=pid2)
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = sprint.objects.get(id = id1).name
        list1=[]
        j=0
        p = sprint.objects.get(id=id1)
        x = p.sprint_start_date
        y = p.sprint_dev_end_date
        x=str(x)
        a,b,c = x.split('-')
        y=str(y)
        d,e,f = y.split('-')
        a=int(a)
        b=int(b)
        c=int(c)
        d=int(d)
        e=int(e)
        f=int(f)
        x=request.user.username
        name1 = user_detail.objects.get(uname=x).name
        data = user_sprint_detail.objects.filter(roles='dev',name=name1,sprint_id=id1)
        name=request.user.username
        list2={}
        n=0
        for i1 in data:
            st1 = story_details.objects.filter(sprint_id=id1,dev_java=name1) | story_details.objects.filter(sprint_id=id1,dev_php=name1) | story_details.objects.filter(sprint_id=id1,dev_html=name1) | story_details.objects.filter(sprint_id=id1,dev_qa=name1)
            list2[name1]={}
            for j11 in st1:
                j1 = story.objects.get(sprint_id=id1,id=j11.story_id)
                if progress.objects.filter(story_id=j1.id,jira_id=j1.jira,dev_name=name1).exists()==True:
                    p1 = progress.objects.filter(story_id=j1.id,jira_id=j1.jira,dev_name=name1).order_by('-id')
                    list2[name1][n]={}
                    for k1 in p1:
                        list2[name1][n][str(k1.work_date)]=str(k1.work_date)
                    n+=1
                else:
                    n+=1
        jd1=json.dumps(list2)
        # print(list2)

        list3={}
        n=0
        st1 = story_details.objects.filter(sprint_id=id1,dev_java=name1) | story_details.objects.filter(sprint_id=id1,dev_php=name1) | story_details.objects.filter(sprint_id=id1,dev_html=name1) | story_details.objects.filter(sprint_id=id1,dev_qa=name1)
        list3[name1]={}
        for j2 in st1:
            j22 = story.objects.get(sprint_id=id1,id=j22.story_id)
            if progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=name1).exists()==True:
                r=0
                p1 = progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=name1).order_by('-id')
                list3[name1][n]={}
                for k2 in p1:
                    list3[name1][n][str(r)]=k2.status
                    r+=1
                    print(k2.status)
                n+=1
            else:
                    n+=1
        jd2=json.dumps(list3)
        # print(list3)

        list4={}
        n=0
        st1 = story_details.objects.filter(sprint_id=id1,dev_java=name1) | story_details.objects.filter(sprint_id=id1,dev_php=name1) | story_details.objects.filter(sprint_id=id1,dev_html=name1) | story_details.objects.filter(sprint_id=id1,dev_qa=name1)
        list4[name1]={}
        for j22 in st1:
            j2 = story.objects.get(sprint_id=id1,id=j22.story_id)
            if progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=name1).exists()==True:
                p1 = progress.objects.filter(story_id=j1.id,jira_id=j2.jira,dev_name=name1).order_by('-id')
                for k2 in p1:
                    list4[name1][n]=k2.jira_id
                    n+=1
            else:
                n+=1
        jd3=json.dumps(list4)

        count=0
        list1.append([])
        k=0
        st = story_details.objects.filter(sprint_id=id1,dev_java=name1) | story_details.objects.filter(sprint_id=id1,dev_php=name1) | story_details.objects.filter(sprint_id=id1,dev_html=name1) | story_details.objects.filter(sprint_id=id1,dev_qa=name1)
        for r in st:
            r1 = story.objects.get(sprint_id=id1,id=r.story_id)
            list1[j].append([])
            list1[j][k].append(r1.story_name)
            list1[j][k].append(r1.jira)
            if r.dev_java==name1:
                list1[j][k].append(r.assigned_java_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.java_points_done)
                if progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_java).exclude(status='').exists()==True:
                    z1 = progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_java).exclude(status='').latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_java_points)-r.java_points_done)
                list1[j][k].append(r1.id)
            elif r.dev_php==name1:
                list1[j][k].append(r.assigned_php_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.php_points_done)
                if progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_php).exclude(status='').exists()==True:
                    z1 = progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_php).exclude(status='').latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_php_points)-r.php_points_done)
                list1[j][k].append(r1.id)
            elif r.dev_html==name1:
                list1[j][k].append(r.assigned_html_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.html_points_done)
                if progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_html).exclude(status='').exists()==True:
                    z1 = progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_html).exclude(status='').latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_html_points)-r.html_points_done)
                list1[j][k].append(r1.id)
            elif r.dev_qa==name1:
                list1[j][k].append(r.assigned_qa_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.qa_points_done)
                if progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_qa).exclude(status='').exists()==True:
                    z1 = progress.objects.filter(story_id=r1.id,jira_id=r1.jira,dev_name=r.dev_qa).exclude(status='').latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_qa_points)-r.qa_points_done)
                list1[j][k].append(r1.id)
            k+=1
            count=count+1;
        j+=1

        if request.method=='GET':
            if 'red' in request.GET:
                idx = request.GET.get('red')
                request.session['story_id'] = idx
                return(redirect('story'))

            if 'as' in request.GET:
                s = request.GET.get('sel')
                j = request.GET.get('jid')
                n1 = request.GET.get('name1')
                p1 = story.objects.filter(sprint_id=id1,jira = j).latest('id')
                p = story_details.objects.get(sprint_id=id1,story_id=p1.id)
                p1.overall_status=s
                p.save()
                return redirect('qaprg')

            if 'bs1' in request.GET:
                if request.user.has_perm("change_progress.change_progress") or ("change_progress") in permission:
                    j = request.GET.get('j1')
                    n2 = request.GET.get('name2')
                    left1 = request.GET.get('left')
                    st = story_details.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                    for ix in st:
                        if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                            pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                            if ix.dev_java==n2:
                                if left1 == (float(ix.assigned_java_points)-ix.java_points_done):
                                    pr1.left= (float(ix.assigned_java_points)-ix.java_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                            elif ix.dev_php==n2:
                                if left1 == (float(ix.assigned_php_points)-ix.php_points_done):
                                    pr1.left= (float(ix.assigned_php_points)-ix.php_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                            elif ix.dev_html==n2:
                                if left1 == (float(ix.assigned_html_points)-ix.html_points_done):
                                    pr1.left= (float(ix.assigned_html_points)-ix.html_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                            else:
                                if left1 == (float(ix.assigned_qa_points)-ix.qa_points_done):
                                    pr1.left= (float(ix.assigned_qa_points)-ix.qa_points_done)
                                    pr1.save()
                                else:
                                    pr1.left=left1
                                    pr1.save()
                        else:
                            messages.info(request, 'No progress recorded as of yet, cannot change points!')
                            return redirect('qaprg')
                else:
                    messages.info(request, 'UNAUTHORIZED!')

                return redirect('qaprg')

            if 'as1' in request.GET:
                stdate = request.GET.get('startdate')
                prog = request.GET.get('prg')
                j = request.GET.get('j1')
                n2 = request.GET.get('name2')
                frac = request.GET.get('fraction')
                frac1=0
                if stdate not in [None,'']:
                    if frac=='Quarter Day':
                        frac1=.5
                    elif frac=='Half Day':
                        frac1=1
                    elif frac=='Three Quarters Day':
                        frac1=1.5
                    else:
                        frac1=2
                    st = story_details.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story_details.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                    cx=0
                    left1=0
                    for ix in st:
                        if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                            pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                            left1 = pr1.left-frac1
                        else:
                            if ix.dev_java==n2:
                                left1 = (float(ix.assigned_java_points)-ix.java_points_done)-frac1
                            elif ix.dev_php==n2:
                                left1 = (float(ix.assigned_php_points)-ix.php_points_done)-frac1
                            elif ix.dev_html==n2:
                                left1 = (float(ix.assigned_html_points)-ix.html_points_done)-frac1
                            else:
                                left1 = (float(ix.assigned_qa_points)-ix.qa_points_done)-frac1
                        if ix.dev_java==n2:
                            ix.java_points_done = ix.java_points_done + frac1
                            if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                cx = pr1.calculated_left - frac1
                            else:
                                cx = float(ix.assigned_java_points)-frac1
                            ix.java_points_left = cx
                        elif ix.dev_php==n2:
                            ix.php_points_done = ix.php_points_done + frac1
                            if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                cx = pr1.calculated_left - frac1
                            else:
                                cx = float(ix.assigned_php_points)-frac1
                            ix.php_points_left = cx
                        elif ix.dev_html==n2:
                            ix.html_points_done = ix.html_points_done + frac1
                            if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                cx = pr1.calculated_left - frac1
                            else:
                                cx = float(ix.assigned_html_points)-frac1
                            ix.html_points_left = cx
                        else:
                            ix.qa_points_done = ix.qa_points_done + frac1
                            if progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').exists()==True:
                                pr1 = progress.objects.filter(story_id=ix.story_id,dev_name=n2).exclude(status='').latest('id')
                                cx = pr1.calculated_left - frac1
                            else:
                                cx = float(ix.assigned_qa_points)-frac1
                            ix.qa_points_left = cx
                        ix.save()
                        z = progress(story_id=ix.story_id,jira_id=j,work_date=stdate,status=prog,dev_name=n2,actual=frac1,left=left1,calculated_left=cx)
                        z.save()

                    list2={}
                    for i1 in data:
                        st1 = story_details.objects.filter(sprint_id=id1,dev_java=i1.name) | story_details.objects.filter(sprint_id=id1,dev_php=i1.name) | story_details.objects.filter(sprint_id=id1,dev_html=i1.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i1.name)
                        n=0
                        list2[i1.name]={}
                        for j11 in st1:
                            j1 = story.objects.get(sprint_id=id1,id=j11.story_id)
                            if progress.objects.filter(story_id=ix.story_id,jira_id=j1.jira,dev_name=i1.name).exists()==True:
                                p1 = progress.objects.filter(story_id=ix.story_id,jira_id=j1.jira,dev_name=i1.name).order_by('-id')
                                for k1 in p1:
                                    list2[i1.name][n]={}
                                    list2[i1.name][n][str(k1.work_date)]=str(k1.work_date)
                                    n+=1

                    jd1=json.dumps(list2)

                    list3={}
                    m=0
                    for i2 in data:
                        st1 = story_details.objects.filter(sprint_id=id1,dev_java=i2.name) | story_details.objects.filter(sprint_id=id1,dev_php=i2.name) | story_details.objects.filter(sprint_id=id1,dev_html=i2.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i2.name)
                        n=0
                        list3[m]={}
                        for j22 in st1:
                            j2 = story.objects.get(sprint_id=id1,id=j22.story_id)
                            if progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                p1 = progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
                                for k2 in p1:
                                    list3[m][n]=k2.status
                                    n+=1
                        m+=1
                    jd2=json.dumps(list3)

                    list4={}
                    m=0
                    for i2 in data:
                        st1 = story_details.objects.filter(sprint_id=id1,dev_java=i2.name) | story_details.objects.filter(sprint_id=id1,dev_php=i2.name) | story_details.objects.filter(sprint_id=id1,dev_html=i2.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i2.name)
                        n=0
                        list4[m]={}
                        for j22 in st1:
                            j2 = story.objects.get(sprint_id=id1,id=j22.story_id)
                            if progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                p1 = progress.objects.filter(story_id=ix.story_id,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
                                for k2 in p1:
                                    list4[m][n]=k2.jira_id
                                    n+=1
                        m+=1
                    jd3=json.dumps(list4)
                else:
                    messages.info(request, 'Please select a Valid Date!')
                return redirect('qaprg')

        if request.method=='POST':
            if 'submit_sprint' in request.POST:
                select = request.POST.get('select_sprint')
                for i in data1:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                return redirect('qaprg')

            if 'select_project' in request.POST:
                name1 = request.POST.get('select_project')
                proid = project.objects.get(name=name1).id
                request.session['pid'] = proid
                spr = sprint.objects.filter(project_id=proid).first()
                request.session['id'] = spr.id
                return redirect('qaprg')

    return(render(request,'qaprg.html/',{'pic':pic,'permission':permission,'name':name,'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'data':data,'list1':list1,'p':p,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'d1':jd1,'d2':jd2,'d3':jd3}))
