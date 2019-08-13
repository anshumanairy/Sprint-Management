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

# sso integration and login security
BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[s[-1]]]

def encryptx(value):
    key = 'NyeRfxLeIrauuHwX'
    cipher = AES.new(key, AES.MODE_ECB)
    beforeCipher = value
    beforeCipher = pad(beforeCipher)
    afterCipher = base64.b64encode(cipher.encrypt(beforeCipher))
    afterCipher = str(afterCipher)
    ac = afterCipher[2:len(afterCipher)-1]
    return(ac)

def decode64(value):
    enc = base64.b64decode(bytes(value, 'utf-8'))
    return enc

def decryptx(value):
    key = 'NyeRfxLeIrauuHwX'
    key_64 = decode64(key)
    return(jwt.decode(value, key_64, algorithms=['HS256']))

# working

@login_required(login_url='/')
def profile(request):
    var=0
    try:
        id1 = request.session['id']
    except Exception as ex:
        messages.info(request, 'Session expired for this ID! Please login again!')
        return(redirect('login'))
    info1 = User.objects.get(username = request.user.username)
    if (User.objects.filter(username=request.user.username, groups__name='Admin').exists() == True):
        info = User.objects.get(username = request.user.username)
        check = 1
    else:
        check=0
        if user_sprint_detail.objects.filter(uname = request.user.username,sprint_id = id1).exists()==True:
            info = user_sprint_detail.objects.get(uname = request.user.username,sprint_id = id1)
        else:
            info = user_detail.objects.get(uname = request.user.username)
    name = request.user.username
    if request.method=='POST':

        if 'update' in request.POST:
            if request.user.is_superuser:
                username = request.POST.get('uname')
                reg1 = User.objects.get(username=request.user.username)
                create = project_details.objects.filter(creator=request.user.username)
                user = authenticate(username = request.user.username , password = 'Zehel9999')
                if user:
                    if username != request.user.username:
                        reg1.username = username
                        reg1.save()
                        for i in create:
                            i.creator=username
                            i.save()
                        messages.info(request, 'Success!')

            else:
                name = request.POST.get('name')
                username = request.POST.get('uname')
                skills = request.POST.getlist('skill[]')
                skill = [item.lower() for item in skills]
                reg1 = User.objects.get(username=request.user.username)
                reg2 = user_detail.objects.get(uname=request.user.username)
                reg3 = user_sprint_detail.objects.filter(uname=request.user.username)
                user = authenticate(username = request.user.username , password = 'Zehel9999')
                if user:
                    if username != request.user.username:
                        reg1.username = username
                        reg2.uname = username
                        reg1.save()
                        reg2.save()
                        for i in reg3:
                            i.uname = username
                            i.save()
                    if name != reg2.name:
                        reg2.name = name
                        reg2.save()
                        for i in reg3:
                            i.name = name
                            i.save()
                    if (reg2.java==False and 'java' in skill) or (reg2.php==False and 'php' in skill) or (reg2.html==False and 'html' in skill) or (reg2.qa==False and 'qa' in skill) or (reg2.java==True and 'java' not in skill) or (reg2.php==True and 'php' not in skill) or (reg2.html==True and 'html' not in skill) or (reg2.qa==True and 'qa' not in skill):
                        reg2.java = False
                        reg2.php = False
                        reg2.html = False
                        reg2.qa = False
                        for j in reg3:
                            j.java = False
                            j.php = False
                            j.html = False
                            j.qa = False
                            j.save()
                        for i in skill:
                            if i == 'java':
                                reg2.java=True
                                for j in reg3:
                                    j.java = True
                                    j.save()
                            if i == 'php':
                                reg2.php=True
                                for j in reg3:
                                    j.php = True
                                    j.save()
                            if i == 'html':
                                reg2.html=True
                                for j in reg3:
                                    j.html = True
                                    j.save()
                            if i == 'qa':
                                reg2.qa=True
                                for j in reg3:
                                    j.qa = True
                                    j.save()
                        reg2.save()

                    messages.info(request, 'Success')

            return(redirect('profile'))

    return render(request,'profile.html/',{'name':name,'info1':info1,'info':info,'check':check,'var':var})

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
        update = progress.objects.filter(story_id=id1,jira_id=stz.jira).order_by('work_date')
        for up in update:
            history.append([])
            dt = up.work_date
            history[h].append(dt.strftime("%Y-%m-%d"))
            history[h].append(up.dev_name)
            if up.actual==0.5:
                history[h].append('Quarter Day')
            elif up.actual==1.0:
                history[h].append('Half Day')
            elif up.actual==1.5:
                history[h].append('Three Quarters Day')
            else:
                history[h].append('Full Day')
            history[h].append(up.status)
            h+=1

        comm={}
        n=0
        for i in st:
            story_comments = comments.objects.filter(story_id=sid)
            comm[n]={}
            for j in story_comments:
                comm[n][j.time_of_comment]={}
                comm[n][j.time_of_comment][j.comment]=j.name
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
                comm = comments(story_id=sid,comment=comment_received,name=request.user.username,time_of_comment=final_time)
                comm.save()
                return redirect('story')

        return render(request,'blog.html/',{'stz':stz,'permission':permission,'history':history,'name':name,'comm':comm,'st':st,'n0':n0,'nx':nx,'nx1':nx1,'data1':data1})
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')

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
                if progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=i1.name).exists()==True:
                    p1 = progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=i1.name).order_by('-id')
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
                if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                    r=0
                    p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
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
                if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                    p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
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
                    if progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_java).exists()==True:
                        z1 = progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_java).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r1.assigned_java_points)-r1.java_points_done)
                elif r1.dev_php==i.name:
                    list1[j][k].append(r1.assigned_php_points)
                    list1[j][k].append(r.overall_status)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r1.php_points_done)
                    list1[j][k].append(float(r1.assigned_php_points)-r1.php_points_done)
                    if progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_php).exists()==True:
                        z1 = progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_php).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r1.assigned_php_points)-r1.php_points_done)
                elif r1.dev_html==i.name:
                    list1[j][k].append(r1.assigned_html_points)
                    list1[j][k].append(r.overall_status)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r1.html_points_done)
                    list1[j][k].append(float(r1.assigned_html_points)-r1.html_points_done)
                    if progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_html).exists()==True:
                        z1 = progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_html).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r.assigned_html_points)-r.html_points_done)
                elif r1.dev_qa==i.name:
                    list1[j][k].append(r1.assigned_qa_points)
                    list1[j][k].append(r.overall_status)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r1.qa_points_done)
                    list1[j][k].append(float(r1.assigned_qa_points)-r1.qa_points_done)
                    if progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_qa).exists()==True:
                        z1 = progress.objects.filter(story_id=id1,jira_id=r.jira,dev_name=r1.dev_qa).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r1.assigned_qa_points)-r1.qa_points_done)

                k+=1
                count=count+1;
            j+=1
        # print(list1)
        name = request.user.username
        if request.method=='GET':

            if 'as' in request.GET:
                s = request.GET.get('sel')
                j = request.GET.get('jid')
                n1 = request.GET.get('name1')
                p1 = story.objects.get(sprint_id=id1,jira = j)
                p = story_details.objects.get(sprint_id=id1,story_id=p1.id)
                p1.overall_status=s
                if request.user.has_perm("change_progress.change_progress") or ("change_progress") in permission:
                    p.save()
                    p1.save()
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
                    left1 = request.GET.get('left')
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
                        for ix in st:
                            if ix.dev_java==n2:
                                if float(left1)==(float(ix.assigned_java_points)-ix.java_points_done):
                                    left1 = (float(ix.assigned_java_points)-(ix.java_points_done+ frac1))
                                ix.java_points_done = ix.java_points_done + frac1
                                ix.java_points_left = left1
                                cx=float(ix.assigned_java_points)-float(left1)
                            elif ix.dev_php==n2:
                                if float(left1)==(float(ix.assigned_php_points)-ix.php_points_done):
                                    left1 = (float(ix.assigned_php_points)-(ix.php_points_done+ frac1))
                                ix.php_points_done = ix.php_points_done + frac1
                                ix.php_points_left = left1
                                cx=float(ix.assigned_php_points)-float(left1)
                            elif ix.dev_html==n2:
                                if float(left1)==(float(ix.assigned_html_points)-ix.html_points_done):
                                    left1 = (float(ix.assigned_html_points)-(ix.html_points_done+ frac1))
                                ix.html_points_done = ix.html_points_done + frac1
                                ix.html_points_left = left1
                                cx=float(ix.assigned_html_points)-float(left1)
                            else:
                                if float(left1)==(float(ix.assigned_qa_points)-ix.qa_points_done):
                                    left1 = (float(ix.assigned_qa_points)-(ix.qa_points_done+ frac1))
                                ix.qa_points_done = ix.qa_points_done + frac1
                                ix.qa_points_left = left1
                                cx=float(ix.assigned_qa_points)-float(left1)
                            ix.save()
                            z = progress(story_id=id1,jira_id=j,work_date=stdate,status=prog,dev_name=n2,actual=frac1,left=left1,calculated_left=cx)
                            z.save()

                        list2={}
                        for i1 in data:
                            st1 = story_details.objects.filter(sprint_id=id1,dev_java=i1.name) | story_details.objects.filter(sprint_id=id1,dev_php=i1.name) | story_details.objects.filter(sprint_id=id1,dev_html=i1.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i1.name)
                            n=0
                            list2[i1.name]={}
                            for j11 in st1:
                                j1 = story.objects.get(sprint_id=id1,id=j11.story_id)
                                if progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=i1.name).exists()==True:
                                    p1 = progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=i1.name).order_by('-id')
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
                                if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                    p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
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
                                if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                    p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
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
                if progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=name1).exists()==True:
                    p1 = progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=name1).order_by('-id')
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
            if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=name1).exists()==True:
                r=0
                p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=name1).order_by('-id')
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
            if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=name1).exists()==True:
                p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=name1).order_by('-id')
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
            r1 = story.objects.get(sprint_id=id1,id=r1.story_id)
            list1[j].append([])
            list1[j][k].append(r1.story_name)
            list1[j][k].append(r1.jira)
            if r.dev_java==name1:
                list1[j][k].append(r.assigned_java_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.java_points_done)
                if progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_java).exists()==True:
                    z1 = progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_java).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_java_points)-r.java_points_done)
            elif r.dev_php==name1:
                list1[j][k].append(r.assigned_php_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.php_points_done)
                if progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_php).exists()==True:
                    z1 = progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_php).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_php_points)-r.php_points_done)
            elif r.dev_html==name1:
                list1[j][k].append(r.assigned_html_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.html_points_done)
                if progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_html).exists()==True:
                    z1 = progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_html).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_html_points)-r.html_points_done)
            elif r.dev_qa==name1:
                list1[j][k].append(r.assigned_qa_points)
                list1[j][k].append(r1.overall_status)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.qa_points_done)
                if progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_qa).exists()==True:
                    z1 = progress.objects.filter(story_id=id1,jira_id=r1.jira,dev_name=r.dev_qa).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.assigned_qa_points)-r.qa_points_done)
            k+=1
            count=count+1;
        j+=1

        if request.method=='GET':
            if 'as' in request.GET:
                s = request.GET.get('sel')
                j = request.GET.get('jid')
                n1 = request.GET.get('name1')
                p1 = story.objects.get(sprint_id=id1,jira = j)
                p = story_details.objects.get(sprint_id=id1,story_id=p1.id)
                p1.overall_status=s
                p.save()
                return redirect('qaprg')

            if 'as1' in request.GET:
                stdate = request.GET.get('startdate')
                prog = request.GET.get('prg')
                j = request.GET.get('j1')
                n2 = request.GET.get('name2')
                frac = request.GET.get('fraction')
                left1 = request.GET.get('left')
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
                    for ix in st:
                        if ix.dev_java==n2:
                            if float(left1)==(float(ix.assigned_java_points)-ix.java_points_done):
                                left1 = (float(ix.assigned_java_points)-(ix.java_points_done+ frac1))
                            ix.java_points_done = ix.java_points_done + frac1
                            ix.java_points_left = left1
                            cx=float(ix.assigned_java_points)-float(left1)
                        elif ix.dev_php==n2:
                            if float(left1)==(float(ix.assigned_php_points)-ix.php_points_done):
                                left1 = (float(ix.assigned_php_points)-(ix.php_points_done+ frac1))
                            ix.php_points_done = ix.php_points_done + frac1
                            ix.php_points_left = left1
                            cx=float(ix.assigned_php_points)-float(left1)
                        elif ix.dev_html==n2:
                            if float(left1)==(float(ix.assigned_html_points)-ix.html_points_done):
                                left1 = (float(ix.assigned_html_points)-(ix.html_points_done+ frac1))
                            ix.html_points_done = ix.html_points_done + frac1
                            ix.html_points_left = left1
                            cx=float(ix.assigned_html_points)-float(left1)
                        else:
                            if float(left1)==(float(ix.assigned_qa_points)-ix.qa_points_done):
                                left1 = (float(ix.assigned_qa_points)-(ix.qa_points_done+ frac1))
                            ix.qa_points_done = ix.qa_points_done + frac1
                            ix.qa_points_left = left1
                            cx=float(ix.assigned_qa_points)-float(left1)
                        ix.save()
                        z = progress(story_id=id1,jira_id=j,work_date=stdate,status=prog,dev_name=n2,actual=frac1,left=left1,calculated_left=cx)
                        z.save()

                    list2={}
                    for i1 in data:
                        st1 = story_details.objects.filter(sprint_id=id1,dev_java=i1.name) | story_details.objects.filter(sprint_id=id1,dev_php=i1.name) | story_details.objects.filter(sprint_id=id1,dev_html=i1.name) | story_details.objects.filter(sprint_id=id1,dev_qa=i1.name)
                        n=0
                        list2[i1.name]={}
                        for j11 in st1:
                            j1 = story.objects.get(sprint_id=id1,id=j11.story_id)
                            if progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=i1.name).exists()==True:
                                p1 = progress.objects.filter(story_id=id1,jira_id=j1.jira,dev_name=i1.name).order_by('-id')
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
                            if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
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
                            if progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).exists()==True:
                                p1 = progress.objects.filter(story_id=id1,jira_id=j2.jira,dev_name=i2.name).order_by('-id')
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

    return(render(request,'qaprg.html/',{'permission':permission,'name':name,'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'data':data,'list1':list1,'p':p,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'d1':jd1,'d2':jd2,'d3':jd3}))

@login_required(login_url='/')
def user_logout(request):
    logout(request)
    # request.session.flush()
    response = redirect('/')
    response.delete_cookie('sessionid', domain="127.0.0.1",path='/')
    response.delete_cookie('csrftoken', domain="127.0.0.1",path='/')
    return response

@login_required(login_url='/')
def prod(request):
    try:
        id = request.session['id']
        pid2 = request.session['pid']
    except Exception as ex:
        messages.info(request, 'Session expired for this ID! Please login again!')
        return(redirect('login'))

    # used to calculate all dates for burndown graph
    list3=[]
    list4=[]
    permission=[]
    per1 = Permission.objects.filter(group__user=request.user)
    for i in per1:
        permission.append(i.name)
    cal=0
    if sprint.objects.filter(id=id,project_id=pid2).exists()==True:
        p1 = sprint.objects.get(id=id,project_id=pid2)
    else:
        p1 = sprint.objects.get(id=0,project_id=0)
    start = p1.sprint_start_date
    if p1.sprint_dev_end_date>=p1.sprint_qa_end_date:
        end = p1.sprint_dev_end_date
        cal = int(p1.dev_working)-1
    else:
        end = p1.sprint_qa_end_date
        cal = int(p1.qa_working)-1
    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    # calculation of total story points assigned in the given sprint
    # list5 stores points in decreasing order and list6 is the average
    list7=[0,0,0,0]
    list5=[]
    list6=[]
    s1 = story_details.objects.filter(sprint_id=id)
    sum1=0
    sum2=0
    sumx=0
    for i1 in s1:
        i2 = story.objects.get(id=i1.story_id)
        sum1 += i1.java_points_left + i1.php_points_left + i1.html_points_left + i1.qa_points_left
        sum2 += i1.assigned_java_points + i1.assigned_php_points + i1.assigned_html_points + i1.assigned_qa_points
        if i2.overall_status in['Pending Deployment','Complete']:
            list7[0]+=1
        elif i2.overall_status in['QA']:
            list7[1]+=1
        elif i2.overall_status in['Live','In Progress','HTML Done','PHP Done','API Done','Blocked','Blocked on API','Blocked on HTML','Blocked on Mock','Blocked on Spec','CR']:
            list7[2]+=1
        else:
            list7[3]+=1
    sumx=sum2
    sumy=sum2
    list5.append(sum2)
    list6.append(sum2)

    for dt in daterange(start, end):
        listz = list(map(str,dt.strftime("%Y-%m-%d").split('-')))
        listzz=[1,4,4,0,2,5,0,3,6,1,4,6]
        s=((int(listz[0])%100)//4)+int(listz[2])+listzz[int(listz[1])-1]+6+(int(listz[0])%100)
        year=int(listz[0])
        z1=0
        if (year % 4) == 0:
           if (year % 100) == 0:
               if (year % 400) == 0:
                   z1=1
               else:
                   z1=0
           else:
               z1=1
        else:
           z1=0

        if z1==1 and (int(listz[1])==1 or int(listz[1])==2):
            s=s-1

        s=s%7
        if s==0 or s==1:
            pass
        else:
            list3.append(dt.strftime("%Y-%m-%d"))
            p2 = progress.objects.filter(story_id=id,work_date=dt.strftime("%Y-%m-%d"))
            s2=0
            s3=0
            s4=0
            s6=0
            for i2 in p2:
                if story_details.objects.filter(sprint_id=id,jira=i2.jira_id).exists()==True:
                    s5 = story_details.objects.get(sprint_id=id,jira=i2.jira_id)
                    if s5.dev_java==i2.dev_name:
                        s4+=s5.assigned_java_points
                    elif s5.dev_php==i2.dev_name:
                        s4+=s5.assigned_php_points
                    elif s5.dev_html==i2.dev_name:
                        s4+=s5.assigned_html_points
                    elif s5.dev_qa==i2.dev_name:
                        s4+=s5.assigned_qa_points

                    s2+=i2.actual
                    s3+=i2.left
                    s6+=i2.calculated_left

            if s2+s3==s4:
                sum2=sum2-s2
                list5.append(sum2)
            else:
                sum2=sum2-s6
                list5.append(sum2)
            if (cal+1)!=0:
                sumx-=(sumy/(cal+1))
                list6.append(sumx)

    # print(list5)
    # print(list6)
    jd1=json.dumps(list3)
    jd5 = json.dumps(list5)
    jd6 = json.dumps(list6)
    jd7 = json.dumps(list7)

    user3 = request.session['user2']
    userxx = request.session['userx']
    s22 = user_sprint_detail.objects.filter(sprint_id=id).exclude(sprint_id=0)
    if sprint.objects.filter(id=id).exists()==True:
        hx2 = sprint.objects.get(id=id).name
    else:
        hx2=''
    if userxx == user3:
        hx1 = user3
        if user_sprint_detail.objects.filter(sprint_id=id,name=user3).exists()==True:
            s2 = user_sprint_detail.objects.get(sprint_id=id,name=user3)
        else:
            s2 = user_sprint_detail.objects.get(sprint_id=0,name='')

        s3 = story_details.objects.filter(sprint_id=id,dev_java=user3) or story_details.objects.filter(sprint_id=id,dev_php=user3) or story_details.objects.filter(sprint_id=id,dev_html=user3) or story_details.objects.filter(sprint_id=id,dev_qa=user3)
        list8=[]
        sp=0
        sc=0
        ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
        for i4 in s3:
            if i4.dev_java==user3:
                sp+=i4.assigned_java_points
                sc+=i4.java_points_done
            elif i4.dev_php==user3:
                sp+=i4.assigned_php_points
                sc+=i4.php_points_done
            elif i4.dev_html==user3:
                sp+=i4.assigned_html_points
                sc+=i4.html_points_done
            elif i4.dev_qa==user3:
                sp+=i4.assigned_qa_points
                sc+=i4.qa_points_done

        list8.append(ab)
        list8.append(sp)
        list8.append(sc)
        jd8 = json.dumps(list8)
        val=json.dumps('Single')
        nval=json.dumps('')

    elif userxx=='Users':
        hx1 = 'All Developers'
        list9=[]
        list10=[]
        userxx = request.session['userx']
        for s2 in s22:
            s3 = story_details.objects.filter(sprint_id=id,dev_java=s2.name) or story_details.objects.filter(sprint_id=id,dev_php=s2.name) or story_details.objects.filter(sprint_id=id,dev_html=s2.name) or story_details.objects.filter(sprint_id=id,dev_qa=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.assigned_java_points
                    sc+=i4.java_points_done
                elif i4.dev_php==s2.name:
                    sp+=i4.assigned_php_points
                    sc+=i4.php_points_done
                elif i4.dev_html==s2.name:
                    sp+=i4.assigned_html_points
                    sc+=i4.html_points_done
                elif i4.dev_qa==s2.name:
                    sp+=i4.assigned_qa_points
                    sc+=i4.qa_points_done
            list9.append(ab)
            list9.append(sp)
            list9.append(sc)
            list10.append(s2.name)
        jd8 = json.dumps(list9)
        val=json.dumps('All Developers')
        nval=json.dumps(list10)

    elif userxx=='Java':
        hx1 = 'Java Dev'
        list9=[]
        list10=[]
        s22 = user_sprint_detail.objects.filter(sprint_id=id,java=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story_details.objects.filter(sprint_id=id,dev_java=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.assigned_java_points
                    sc+=i4.java_points_done
                elif i4.dev_php==s2.name:
                    sp+=i4.assigned_php_points
                    sc+=i4.php_points_done
                elif i4.dev_html==s2.name:
                    sp+=i4.assigned_html_points
                    sc+=i4.html_points_done
                elif i4.dev_qa==s2.name:
                    sp+=i4.assigned_qa_points
                    sc+=i4.qa_points_done
            list9.append(ab)
            list9.append(sp)
            list9.append(sc)
            list10.append(s2.name)
        jd8 = json.dumps(list9)
        val=json.dumps('Java Dev')
        nval=json.dumps(list10)

    elif userxx=='PHP':
        hx1 = 'PHP Dev'
        list9=[]
        list10=[]
        s22 = user_sprint_detail.objects.filter(sprint_id=id,php=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story_details.objects.filter(sprint_id=id,dev_php=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.assigned_java_points
                    sc+=i4.java_points_done
                elif i4.dev_php==s2.name:
                    sp+=i4.assigned_php_points
                    sc+=i4.php_points_done
                elif i4.dev_html==s2.name:
                    sp+=i4.assigned_html_points
                    sc+=i4.html_points_done
                elif i4.dev_qa==s2.name:
                    sp+=i4.assigned_qa_points
                    sc+=i4.qa_points_done
            list9.append(ab)
            list9.append(sp)
            list9.append(sc)
            list10.append(s2.name)
        jd8 = json.dumps(list9)
        val=json.dumps('PHP Dev')
        nval=json.dumps(list10)

    elif userxx=='HTML':
        hx1 = 'HTML Dev'
        list9=[]
        list10=[]
        s22 = user_sprint_detail.objects.filter(sprint_id=id,html=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story_details.objects.filter(sprint_id=id,dev_html=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.assigned_java_points
                    sc+=i4.java_points_done
                elif i4.dev_php==s2.name:
                    sp+=i4.assigned_php_points
                    sc+=i4.php_points_done
                elif i4.dev_html==s2.name:
                    sp+=i4.assigned_html_points
                    sc+=i4.html_points_done
                elif i4.dev_qa==s2.name:
                    sp+=i4.assigned_qa_points
                    sc+=i4.qa_points_done
            list9.append(ab)
            list9.append(sp)
            list9.append(sc)
            list10.append(s2.name)
        jd8 = json.dumps(list9)
        val=json.dumps('HTML Dev')
        nval=json.dumps(list10)

    elif userxx=='QA':
        hx1 = 'QA Dev'
        list9=[]
        list10=[]
        s22 = user_sprint_detail.objects.filter(sprint_id=id,qa=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story_details.objects.filter(sprint_id=id,dev_qa=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.assigned_java_points
                    sc+=i4.java_points_done
                elif i4.dev_php==s2.name:
                    sp+=i4.assigned_php_points
                    sc+=i4.php_points_done
                elif i4.dev_html==s2.name:
                    sp+=i4.assigned_html_points
                    sc+=i4.html_points_done
                elif i4.dev_qa==s2.name:
                    sp+=i4.assigned_qa_points
                    sc+=i4.qa_points_done
            list9.append(ab)
            list9.append(sp)
            list9.append(sc)
            list10.append(s2.name)
        jd8 = json.dumps(list9)
        val=json.dumps('QA Dev')
        nval=json.dumps(list10)

    data = sprint.objects.filter(project_id=pid2)
    n = project.objects.all().exclude(id=0)
    if project.objects.filter(id=pid2).exists()==True:
        nx = project.objects.get(id=pid2)
    else:
        nx=''
    form = sprintform(request.POST or None)
    list11=[]
    z1 = User.objects.all()
    for i11 in z1:
        if i11.is_superuser:
            list11.append(i11.username)

    z2 = user_detail.objects.all()
    name = request.user.username
    if request.method=='POST':
        #select sprint get value and redirect
        if 'select_sprint' in request.POST:
            select = request.POST.get('select_sprint')

            if select==None:
                messages.info(request, 'Please select a Valid Sprint!')
                return redirect('product')
            else:
                for i in data:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                list3=[]
                p1 = sprint.objects.get(id=id,project_id=pid2)
                start = p1.sprint_start_date
                end = p1.sprint_dev_end_date
                def daterange(date1, date2):
                    for n in range(int ((date2 - date1).days)+1):
                        yield date1 + timedelta(n)
                for dt in daterange(start, end):
                    list3.append(dt.strftime("%Y-%m-%d"))
                jd1=json.dumps(list3)
                return redirect('product')

        if 'project_button' in request.POST:
            name1 = request.POST.get('pname')
            user1 = request.POST.get('select_admin')
            listz1 = request.POST.getlist('select_users[]')
            listz2 = request.POST.getlist('select_manager[]')
            c=''
            for x in listz1:
                c+=x+'@end@'
            d=''
            for y in listz2:
                d+=y+'@end@'
            n = project.objects.all().exclude(id=0)
            a=0
            for i in n:
                if name1==i.name:
                    a+=1
                    messages.info(request, 'Project Name already taken. Please choose another one!')
                    return redirect('product')
            if a==0:
                z = project(name = name1)
                z.save()
                z1 = project.objects.latest('id')
                z2 = project_details(project_id=z1.id,creator=user1,devs=c,mans=d)
                if request.user.has_perm("add_project.add_project") or ("add_project") in permission:
                    z2.save()
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('product')
            return(redirect('product'))

        if 'select_project' in request.POST:
            name1 = request.POST.get('select_project')
            proid = project.objects.get(name=name1).id
            request.session['pid'] = proid
            if sprint.objects.filter(project_id=proid).exists()==True:
                spr = sprint.objects.filter(project_id=proid).first()
                request.session['id'] = spr.id
            else:
                request.session['id'] = 0
            return(redirect('product'))

        if 'select_user' in request.POST:
            user1 = request.POST.get('select_user')
            if user1 not in ['All Developers','Java Dev','PHP Dev','HTML Dev','QA Dev']:
                request.session['user2'] = user1
                request.session['userx'] = user1
                s2 = user_sprint_detail.objects.get(sprint_id=id,name=user1)
                s3 = story_details.objects.filter(sprint_id=id,dev_java=user1) or story_details.objects.filter(sprint_id=id,dev_php=user1) or story_details.objects.filter(sprint_id=id,dev_html=user1) or story_details.objects.filter(sprint_id=id,dev_qa=user1)
                list8=[]
                sp=0
                sc=0
                ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                for i4 in s3:
                    if i4.dev_java==user1:
                        sp+=i4.assigned_java_points
                        sc+=i4.java_points_done
                    elif i4.dev_php==user1:
                        sp+=i4.assigned_php_points
                        sc+=i4.php_points_done
                    elif i4.dev_html==user1:
                        sp+=i4.assigned_html_points
                        sc+=i4.html_points_done
                    elif i4.dev_qa==user1:
                        sp+=i4.assigned_qa_points
                        sc+=i4.qa_points_done
                list8.append(ab)
                list8.append(sp)
                list8.append(sc)
                jd8 = json.dumps(list8)
                nval=json.dumps('')
                val=json.dumps('Single')

            if user1 == "All Developers":
                request.session['userx'] = 'Users'
                s22 = user_sprint_detail.objects.filter(sprint_id=id).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story_details.objects.filter(sprint_id=id,dev_java=s2.name) or story_details.objects.filter(sprint_id=id,dev_php=s2.name) or story_details.objects.filter(sprint_id=id,dev_html=s2.name) or story_details.objects.filter(sprint_id=id,dev_qa=s2.name)
                    sp=0
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.assigned_java_points
                            sc+=i4.java_points_done
                        elif i4.dev_php==s2.name:
                            sp+=i4.assigned_php_points
                            sc+=i4.php_points_done
                        elif i4.dev_html==s2.name:
                            sp+=i4.assigned_html_points
                            sc+=i4.html_points_done
                        elif i4.dev_qa==s2.name:
                            sp+=i4.assigned_qa_points
                            sc+=i4.qa_points_done
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('All Developers')
                    nval=json.dumps(list10)

            if user1 == "Java Dev":
                request.session['userx'] = 'Java'
                s22 = user_sprint_detail.objects.filter(sprint_id=id,java=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story_details.objects.filter(sprint_id=id,dev_java=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.assigned_java_points
                            sc+=i4.java_points_done
                        elif i4.dev_php==s2.name:
                            sp+=i4.assigned_php_points
                            sc+=i4.php_points_done
                        elif i4.dev_html==s2.name:
                            sp+=i4.assigned_html_points
                            sc+=i4.html_points_done
                        elif i4.dev_qa==s2.name:
                            sp+=i4.assigned_qa_points
                            sc+=i4.qa_points_done
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('Java Dev')
                    nval=json.dumps(list10)

            if user1 == "PHP Dev":
                request.session['userx'] = 'PHP'
                s22 = user_sprint_detail.objects.filter(sprint_id=id,php=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story_details.objects.filter(sprint_id=id,dev_php=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.assigned_java_points
                            sc+=i4.java_points_done
                        elif i4.dev_php==s2.name:
                            sp+=i4.assigned_php_points
                            sc+=i4.php_points_done
                        elif i4.dev_html==s2.name:
                            sp+=i4.assigned_html_points
                            sc+=i4.html_points_done
                        elif i4.dev_qa==s2.name:
                            sp+=i4.assigned_qa_points
                            sc+=i4.qa_points_done
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('PHP Dev')
                    nval=json.dumps(list10)

            if user1 == "HTML Dev":
                request.session['userx'] = 'HTML'
                s22 = user_sprint_detail.objects.filter(sprint_id=id,html=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story_details.objects.filter(sprint_id=id,dev_html=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.assigned_java_points
                            sc+=i4.java_points_done
                        elif i4.dev_php==s2.name:
                            sp+=i4.assigned_php_points
                            sc+=i4.php_points_done
                        elif i4.dev_html==s2.name:
                            sp+=i4.assigned_html_points
                            sc+=i4.html_points_done
                        elif i4.dev_qa==s2.name:
                            sp+=i4.assigned_qa_points
                            sc+=i4.qa_points_done
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('HTML Dev')
                    nval=json.dumps(list10)

            if user1 == "QA Dev":
                request.session['userx'] = 'QA'
                s22 = user_sprint_detail.objects.filter(sprint_id=id,qa=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story_details.objects.filter(sprint_id=id,dev_qa=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.assigned_java_points
                            sc+=i4.java_points_done
                        elif i4.dev_php==s2.name:
                            sp+=i4.assigned_php_points
                            sc+=i4.php_points_done
                        elif i4.dev_html==s2.name:
                            sp+=i4.assigned_html_points
                            sc+=i4.html_points_done
                        elif i4.dev_qa==s2.name:
                            sp+=i4.assigned_qa_points
                            sc+=i4.qa_points_done
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('QA Dev')
                    nval=json.dumps(list10)

            return(redirect('product'))

        # productform condition where sprint_button is the name for submit button for sprint form
        if 'sprint_button' in request.POST:
            start = request.POST.get('start')
            dev = request.POST.get('dev')
            qa = request.POST.get('qa')
            if (User.objects.filter(username=request.user.username, groups__name='Admin').exists() == True) or (user_sprint_detail.objects.filter(uname=request.user.username,sprint_id=id,roles='man').exists()==True):
                if form.is_valid():
                    form = sprintform(request.POST)
                    form.instance.project_id = pid2
                    form.instance.sprint_start_date=start
                    form.instance.sprint_dev_end_date=dev
                    form.instance.sprint_qa_end_date=qa
                    form.save()
                    x = form.instance.id
                    x1 = user_detail.objects.all()
                    obj = project_details.objects.get(project_id=pid2)
                    selected_users = list(map(str,(obj.devs).split('@end@')))
                    selected_mans = list(map(str,(obj.mans).split('@end@')))
                    for i1 in x1:
                        if i1.uname in selected_mans:
                            x2 = user_sprint_detail(sprint_id=x,uname=i1.uname,name=i1.name,roles='man',java=i1.java,html=i1.html,php=i1.php,qa=i1.php)
                            if request.user.has_perm("add_sprint.add_sprint") or ("add_sprint") in permission:
                                x2.save()
                            else:
                                messages.info(request, 'UNAUTHORIZED!')
                                return redirect('product')
                        else:
                            if i1.uname in selected_users:
                                x2 = user_sprint_detail(sprint_id=x,uname=i1.uname,name=i1.name,roles=i1.roles,java=i1.java,html=i1.html,php=i1.php,qa=i1.php)
                                if request.user.has_perm("add_sprint.add_sprint") or ("add_sprint") in permission:
                                    x2.save()
                                else:
                                    messages.info(request, 'UNAUTHORIZED!')
                                    return redirect('product')
                    return redirect('product')
                else:
                    messages.info(request, 'Data Not Stored!')
                    return redirect('product')
            else:
                messages.info(request, 'You are not Authorized!')
                return redirect('product')
        else:
            form = sprintform()

    return(render(request,'product.html/',context={'permission':permission,'name':name,'z2':z2,'nval':nval,'val':val,'hx2':hx2,'hx1':hx1,'jd8':jd8,'s22':s22,'jd7':jd7,'jd6':jd6,'jd5':jd5,'jd1':jd1,'form':form,'data':data,'n':n,'nx':nx,'list11':list11}))

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
    for i in per1:
        permission.append(i.name)
    if request.user.has_perm("view_stories.view_stories") or ("view_stories") in permission:
        data1 = sprint.objects.filter(project_id=pid2)
        n = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
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
        sjava = user_sprint_detail.objects.aggregate(Sum('spjava'))['spjava__sum']
        sphp = user_sprint_detail.objects.aggregate(Sum('spphp'))['spphp__sum']
        shtml = user_sprint_detail.objects.aggregate(Sum('sphtml'))['sphtml__sum']
        sqa = user_sprint_detail.objects.aggregate(Sum('spqa'))['spqa__sum']
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
                p = story.objects.get(sprint_id=id,jira=soj)
                p.story_name = sn
                p.description = sd
                p.jira = snj
                if request.user.has_perm("edit_story.edit_story") or ("edit_story") in permission:
                    p.save()
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('view_story')
                return(redirect('view_story'))

            if 'assign_data' in request.GET:
                if request.user.has_perm("allocate_points.allocate_points") or ("allocate_points") in permission:
                    java_dev = request.GET.get('java_sel')
                    p1 = request.GET.get('points1')
                    idy = request.GET.get('idx')
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
                                if q.overall_status in [None,'']:
                                    q.overall_status='Live'
                                p.save()
                        a=sum(list1)

                        # user change
                        try:
                            if dev1 != None and dev1 != java_dev :
                                creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                                creg1 = user_sprint_detail.objects.get(name=java_dev,sprint_id=id)
                                j = story_details.objects.filter(sprint_id=id, dev_java=dev1)
                                j1 = story_details.objects.filter(sprint_id=id, dev_java=java_dev)

                                if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                                    creg.djava = creg.spjava
                                else:
                                    creg.djava = creg.spjava - (j1.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])

                                if j1.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                                    creg1.djava = creg1.spjava
                                else:
                                    creg1.djava = creg1.spjava - (j1.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])

                                creg.save()
                                creg1.save()

                                pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira)
                                for p1 in pr:
                                    p1.dev_name = java_dev
                                    p1.save()
                        except:
                            pass

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
                                if q.overall_status in [None,'']:
                                    q.overall_status='Live'
                                p.save()
                        b=sum(list2)

                        if dev1 != None and dev1 != php_dev :
                            creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                            creg1 = user_sprint_detail.objects.get(name=php_dev,sprint_id=id)
                            j = story_details.objects.filter(sprint_id=id, dev_php=dev1)
                            j1 = story_details.objects.filter(sprint_id=id, dev_php=php_dev)

                            if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                                creg.dphp = creg.spphp
                            else:
                                creg.dphp = creg.spphp - (j1.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])

                            if j1.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                                creg1.dphp = creg1.spphp
                            else:
                                creg1.dphp = creg1.spphp - (j1.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])

                            creg.save()
                            creg1.save()

                            pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira)
                            for p1 in pr:
                                p1.dev_name = php_dev
                                p1.save()

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
                                if q.overall_status in [None,'']:
                                    q.overall_status='Live'
                                p.save()
                        c=sum(list3)

                        # user change
                        if dev1 != None and dev1 != html_dev :
                            creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                            creg1 = user_sprint_detail.objects.get(name=html_dev,sprint_id=id)
                            j = story_details.objects.filter(sprint_id=id, dev_html=dev1)
                            j1 = story_details.objects.filter(sprint_id=id, dev_html=html_dev)

                            if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                                creg.dhtml = creg.sphtml
                            else:
                                creg.dhtml = creg.sphtml - (j1.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])

                            if j1.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                                creg1.dhtml = creg1.sphtml
                            else:
                                creg1.dhtml = creg1.sphtml - (j1.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])

                            creg.save()
                            creg1.save()

                            pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira)
                            for p1 in pr:
                                p1.dev_name = html_dev
                                p1.save()

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
                                if q.overall_status in [None,'']:
                                    q.overall_status='Live'
                                p.save()
                        d=sum(list4)

                        # user change
                        if dev1 != None and dev1 != qa_dev :
                            creg = user_sprint_detail.objects.get(name=dev1,sprint_id=id)
                            creg1 = user_sprint_detail.objects.get(name=qa_dev,sprint_id=id)
                            j = story_details.objects.filter(sprint_id=id, dev_qa=dev1)
                            j1 = story_details.objects.filter(sprint_id=id, dev_qa=qa_dev)

                            if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                                creg.dqa = creg.spqa
                            else:
                                creg.dqa = creg.spqa - (j1.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])

                            if j1.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                                creg1.dqa = creg1.spqa
                            else:
                                creg1.dqa = creg1.spqa - (j1.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])

                            creg.save()
                            creg1.save()

                            pr = progress.objects.filter(dev_name=dev1,story_id=id,jira_id=p.jira)
                            for p1 in pr:
                                p1.dev_name = qa_dev
                                p1.save()

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
                                    z2 = story.objects.get(sprint_id=id,story_name=fields[0],description=fields[1],jira=fields[2],overall_status=fields[11])
                                    z3 = story_details(sprint_id=id,jira=fields[2],story_id=z2.id,dev_java=fields[3],assigned_java_points=int(fields[4]),dev_php=fields[5],assigned_php_points=int(fields[6]),dev_html=fields[7],assigned_html_points=int(fields[8]),dev_qa=fields[9],assigned_qa_points=int(fields[10]))
                                    if request.user.has_perm("add_story.add_story") or ("add_story") in permission:
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
                    for i in p:
                        if form.instance.jira == i.jira:
                            messages.info(request, 'Jira ID already exists. Please choose another one!')
                            return redirect('view_story')
                    form.save()
                    z4 = story.objects.latest('id')
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

        return render(request,'view_story.html',{'permission':permission,'datay':datay,'jd8x':jd8x,'jd7x':jd7x,'jd6x':jd6x,'jd5x':jd5x,'jd4x':jd4x,'jd3x':jd3x,'aa':aa,'bb':bb,'cc':cc,'dd':dd,'ee':ee,'ff':ff,'jd1x':jd1x,'jd2x':jd2x,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'dashboard':dashboard,'list11':list11,'list21':list21,'list31':list31,'list41':list41,'a':a,'b':b,'c':c,'d':d,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'d1':d1,'form':form,'data':data,'jd1':jd1,'jd2':jd2,'jd3':jd3,'jd4':jd4,'n':n,'nx':nx,'data1':data1,'nx1':nx1,'name':name,'dashboard1':dashboard1})
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')

@login_required(login_url='/')
def bandwidth(request):
    try:
        sprid = request.session['id']
        pid2 = request.session['pid']
    except Exception as ex:
        messages.info(request, 'Session expired for this ID! Please login again!')
        return(redirect('login'))
    if sprid==0 or pid2==0:
        messages.info(request, 'Select a valid sprint and project first!')
        return redirect('product')
    permission=[]
    per1 = Permission.objects.filter(group__user=request.user)
    for i in per1:
        permission.append(i.name)
    if request.user.has_perm("view_bandwidth.view_bandwidth") or ("view_bandwidth") in permission:
        data1 = sprint.objects.filter(project_id=pid2)
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = sprint.objects.get(id = sprid).name
        sjava = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('spjava'))['spjava__sum']
        sphp = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('spphp'))['spphp__sum']
        shtml = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('sphtml'))['sphtml__sum']
        sqa = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('spqa'))['spqa__sum']
        band = sprint.objects.filter(id=sprid)
        data = story.objects.filter(sprint_id=sprid)
        d1 = user_sprint_detail.objects.filter(roles='dev')
        d2 = user_sprint_detail.objects.filter(roles='dev',java='True',sprint_id=sprid)
        d3 = user_sprint_detail.objects.filter(roles='dev',php='True',sprint_id=sprid)
        d4 = user_sprint_detail.objects.filter(roles='dev',html='True',sprint_id=sprid)
        d5 = user_sprint_detail.objects.filter(roles='dev',qa='True',sprint_id=sprid)

        list1=[]
        for i in d2:
            j = story_details.objects.filter(sprint_id=sprid, dev_java=i.name)
            r = user_sprint_detail.objects.get(roles='dev',java='True',name=i.name,sprint_id=sprid)
            if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                list1.append(0)
                r.djava = r.spjava
            else:
                list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                r.djava = r.spjava - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
            r.save()


        list2=[]
        for i in d3:
            j = story_details.objects.filter(sprint_id=sprid, dev_php=i.name)
            r = user_sprint_detail.objects.get(roles='dev',php='True',name=i.name,sprint_id=sprid)
            if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                list2.append(0)
                r.dphp = r.spphp
            else:
                list2.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                r.dphp = r.spphp - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
            r.save()

        list3=[]
        for i in d4:
            j = story_details.objects.filter(sprint_id=sprid, dev_html=i.name)
            r = user_sprint_detail.objects.get(roles='dev',html='True',name=i.name,sprint_id=sprid)
            if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                list3.append(0)
                r.dhtml = r.sphtml
            else:
                list3.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                r.dhtml = r.sphtml - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
            r.save()

        list4=[]
        for i in d5:
            j = story_details.objects.filter(sprint_id=sprid, dev_qa=i.name)
            r = user_sprint_detail.objects.get(roles='dev',qa='True',name=i.name,sprint_id=sprid)
            if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                list4.append(0)
                r.dqa = r.spqa
            else:
                list4.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                r.dqa = r.spqa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
            r.save()

        x = sprint.objects.get(id=sprid)
        day1 = (x.sprint_start_date + timedelta(x1 + 1) for x1 in range((x.sprint_dev_end_date - x.sprint_start_date).days))
        y = sum(1 for day in day1 if day.weekday() < 5)

        day2 = (x.sprint_start_date + timedelta(x1 + 1) for x1 in range((x.sprint_qa_end_date - x.sprint_start_date).days))
        z = sum(1 for day in day2 if day.weekday() < 5)

        y = y - x.holidays
        z = z - x.holidays
        x.dev_working = y
        x.qa_working = z
        x.save()
        name=request.user.username

        if request.method=='GET':
            if 'assign1' in request.GET:
                if request.user.has_perm("change_bandwidth.change_bandwidth") or ("change_bandwidth") in permission:
                    vf = request.GET.get('assign1')
                    uid = request.GET.get('assign2')
                    skill = request.GET.get('assign3')
                    p = sprint.objects.get(id=sprid)

                    if skill == 'java':
                        r = user_sprint_detail.objects.get(id=uid, java='True',sprint_id=sprid)
                        r.vfjava = vf
                        ab = (float(vf) * (p.dev_working-r.planned-r.unplanned))
                        r.abjava = int(ab)
                        r.spjava = r.abjava * 2
                        sjava = user_sprint_detail.objects.aggregate(Sum('spjava'))['spjava__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_java=r.name)
                        if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                            list1.append(0)
                            r.djava = r.spjava
                        else:
                            list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.djava = r.spjava - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])


                    if skill == 'php':
                        r = user_sprint_detail.objects.get(id=uid, php='True',sprint_id=sprid)
                        r.vfphp = vf
                        ab = (float(vf) * (p.dev_working-r.planned-r.unplanned))
                        r.abphp = int(ab)
                        r.spphp = r.abphp * 2
                        sphp = user_sprint_detail.objects.aggregate(Sum('spphp'))['spphp__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_php=r.name)
                        if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                            list1.append(0)
                            r.dphp = r.spphp
                        else:
                            list1.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.dphp = r.spphp - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])


                    if skill == 'html':
                        r = user_sprint_detail.objects.get(id=uid, html='True',sprint_id=sprid)
                        r.vfhtml = vf
                        ab = (float(vf) * (p.dev_working-r.planned-r.unplanned))
                        r.abhtml = int(ab)
                        r.sphtml = r.abhtml * 2
                        shtml = user_sprint_detail.objects.aggregate(Sum('sphtml'))['sphtml__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_html=r.name)
                        if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                            list1.append(0)
                            r.dhtml = r.sphtml
                        else:
                            list1.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.dhtml = r.sphtml - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])



                    if skill == 'qa':
                        r = user_sprint_detail.objects.get(id=uid, qa='True',sprint_id=sprid)
                        r.vfqa = vf
                        ab = (float(vf) * (p.qa_working-r.planned-r.unplanned))
                        r.abqa = int(ab)
                        r.spqa = r.abqa * 2
                        sqa = user_sprint_detail.objects.aggregate(Sum('spqa'))['spqa__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_qa=r.name)
                        if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                            list1.append(0)
                            r.dqa = r.spqa
                        else:
                            list1.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.dqa = r.spqa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])

                    r.save()
                    return redirect('/bandwidth/')
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('/bandwidth/')


            if 'uleave1' in request.GET:
                if request.user.has_perm("change_bandwidth.change_bandwidth") or ("change_bandwidth") in permission:
                    pl = request.GET.get('uleave1')
                    uid = request.GET.get('uleave2')
                    skill = request.GET.get('uleave3')
                    r = user_sprint_detail.objects.get(id=uid,sprint_id=sprid)
                    r.unplanned = int(pl)
                    p = sprint.objects.get(id=sprid)
                    d2 = user_sprint_detail.objects.filter(roles='dev',java='True',sprint_id=sprid)
                    d3 = user_sprint_detail.objects.filter(roles='dev',php='True',sprint_id=sprid)
                    d4 = user_sprint_detail.objects.filter(roles='dev',html='True',sprint_id=sprid)
                    d5 = user_sprint_detail.objects.filter(roles='dev',qa='True',sprint_id=sprid)
                    r.save()

                    if skill=='java':
                        r = user_sprint_detail.objects.get(id=uid,java='True',sprint_id=sprid)
                        ab = (r.vfjava)*(p.dev_working-r.planned-r.unplanned)
                        r.abjava=ab
                        r.spjava = r.abjava * 2
                        sjava = user_sprint_detail.objects.aggregate(Sum('spjava'))['spjava__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_java=r.name)
                        if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                            list1.append(0)
                            r.djava = r.spjava
                        else:
                            list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.djava = r.spjava - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])

                            r.save()


                    if skill=='php':
                        r = user_sprint_detail.objects.get(id=uid,php='True',sprint_id=sprid)
                        ab = (r.vfphp)*(p.dev_working-r.planned-r.unplanned)
                        r.abphp=ab
                        r.spphp = r.abphp * 2
                        sphp = user_sprint_detail.objects.aggregate(Sum('spphp'))['spphp__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_php=r.name)
                        if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                            list1.append(0)
                            r.dphp = r.spphp
                        else:
                            list1.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.dphp = r.spphp - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.save()


                    if skill=='html':
                        r = user_sprint_detail.objects.get(id=uid,html='True',sprint_id=sprid)
                        ab = (r.vfhtml)*(p.dev_working-r.planned-r.unplanned)
                        r.abhtml=ab
                        r.sphtml = r.abhtml * 2
                        shtml = user_sprint_detail.objects.aggregate(Sum('sphtml'))['sphtml__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_html=r.name)
                        if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                            list1.append(0)
                            r.dhtml = r.sphtml
                        else:
                            list1.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.dhtml = r.sphtml - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.save()

                    if skill=='qa':
                        r = user_sprint_detail.objects.get(id=uid,qa='True',sprint_id=sprid)
                        ab = (r.vfqa)*(p.qa_working-r.planned-r.unplanned)
                        r.abqa=ab
                        r.spqa = r.abqa * 2
                        sqa = user_sprint_detail.objects.aggregate(Sum('spqa'))['spqa__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_qa=r.name)
                        if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                            list1.append(0)
                            r.dqa = r.spqa
                        else:
                            list1.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.dqa = r.spqa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.save()
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('bandwidth')


            if 'leave1' in request.GET:
                if request.user.has_perm("change_bandwidth.change_bandwidth") or ("change_bandwidth") in permission:
                    pl = request.GET.get('leave1')
                    uid = request.GET.get('leave2')
                    skill = request.GET.get('leave3')
                    r = user_sprint_detail.objects.get(id=uid,sprint_id=sprid)
                    r.planned = int(pl)
                    p = sprint.objects.get(id=sprid)
                    d2 = user_sprint_detail.objects.filter(roles='dev',java='True',sprint_id=sprid)
                    d3 = user_sprint_detail.objects.filter(roles='dev',php='True',sprint_id=sprid)
                    d4 = user_sprint_detail.objects.filter(roles='dev',html='True',sprint_id=sprid)
                    d5 = user_sprint_detail.objects.filter(roles='dev',qa='True',sprint_id=sprid)
                    r.save()

                    if skill=='java':
                        r = user_sprint_detail.objects.get(id=uid,java='True',sprint_id=sprid)
                        ab = (r.vfjava)*(p.dev_working-r.planned-r.unplanned)
                        r.abjava=ab
                        r.spjava = r.abjava * 2
                        sjava = user_sprint_detail.objects.aggregate(Sum('spjava'))['spjava__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_java=r.name)
                        if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                            list1.append(0)
                            r.djava = r.spjava
                        else:
                            list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.djava = r.spjava - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.save()


                    if skill=='php':
                        r = user_sprint_detail.objects.get(id=uid,php='True',sprint_id=sprid)
                        ab = (r.vfphp)*(p.dev_working-r.planned-r.unplanned)
                        r.abphp=ab
                        r.spphp = r.abphp * 2
                        sphp = user_sprint_detail.objects.aggregate(Sum('spphp'))['spphp__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_php=r.name)
                        if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                            list1.append(0)
                            r.dphp = r.spphp
                        else:
                            list1.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.dphp = r.spphp - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.save()


                    if skill=='html':
                        r = user_sprint_detail.objects.get(id=uid,html='True',sprint_id=sprid)
                        ab = (r.vfhtml)*(p.dev_working-r.planned-r.unplanned)
                        r.abhtml=ab
                        r.sphtml = r.abhtml * 2
                        shtml = user_sprint_detail.objects.aggregate(Sum('sphtml'))['sphtml__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_html=r.name)
                        if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                            list1.append(0)
                            r.dhtml = r.sphtml
                        else:
                            list1.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.dhtml = r.sphtml - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.save()

                    if skill=='qa':
                        r = user_sprint_detail.objects.get(id=uid,qa='True',sprint_id=sprid)
                        ab = (r.vfqa)*(p.qa_working-r.planned-r.unplanned)
                        r.abqa=ab
                        r.spqa = r.abqa * 2
                        sqa = user_sprint_detail.objects.aggregate(Sum('spqa'))['spqa__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_qa=r.name)
                        if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                            list1.append(0)
                            r.dqa = r.spqa
                        else:
                            list1.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.dqa = r.spqa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.save()
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('bandwidth')

        if request.method=='POST':
            if 'select_sprint' in request.POST:
                select = request.POST.get('select_sprint')
                for i in data1:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                return redirect('bandwidth')

            if 'select_project' in request.POST:
                name1 = request.POST.get('select_project')
                proid = project.objects.get(name=name1).id
                request.session['pid'] = proid
                spr = sprint.objects.filter(project_id=proid).first()
                request.session['id'] = spr.id
                return redirect('bandwidth')

        return(render(request,'bandwidth.html/',{'permission':permission,'name':name,'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'band':band,'d1':d1,'data':data,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'list1':list1,'list2':list2,'list3':list3,'list4':list4}))
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')

@login_required(login_url='/')
def tasks(request):
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
    for i in per1:
        permission.append(i.name)
    if request.user.has_perm("view_report.view_report") or ("view_report") in permission:
        data1 = sprint.objects.filter(project_id=pid2)
        data3 = sprint.objects.filter(project_id=pid2).exclude(id=id1)
        list1x=[]
        list2x=[]
        list3x=[]

        check=0
        if request.user.is_superuser or (user_sprint_detail.objects.filter(uname=request.user.username,sprint_id=id1,roles='man').exists()==True):
            check=1
            pass
        else:
            u1 = user_detail.objects.get(uname=request.user.username)
            for i in data1:
                st = story.objects.filter(sprint_id=i.id)
                for j in st:
                    list1x.append(i.name)
                    list2x.append(j.jira)
            if u1.java==True:
                list3x.append('Java')
            if u1.php==True:
                list3x.append('PHP')
            if u1.html==True:
                list3x.append('HTML')
            if u1.qa==True:
                list3x.append('QA')

        jd1x=json.dumps(list1x)
        jd2x=json.dumps(list2x)
        jd3x=json.dumps(list3x)

        listse=[]
        k1 = project.objects.all().exclude(id=0)
        n=0
        for k2 in k1:
            listse.append([])
            k3 = sprint.objects.filter(project_id=k2.id).exclude(id=id1)
            m=0
            for k4 in k3:
                if k4.sprint_dev_end_date>=k4.sprint_qa_end_date:
                    if k4.sprint_dev_end_date>=datetime.date.today():
                        listse[n].append([])
                        listse[n][m].append(k4.name)
                        listse[n][m].append(k4.id)
                        m+=1
                else:
                    if k4.sprint_qa_end_date>=datetime.date.today():
                        listse[n].append([])
                        listse[n][m].append(k4.name)
                        listse[n][m].append(k4.id)
                        m+=1
            n+=1
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = sprint.objects.get(id = id1).name
        pro = sprint.objects.filter(project_id=pid2)


        k=0
        repo=[]
        c1 = user_sprint_detail.objects.filter(sprint_id=id1,roles='dev')
        sum3=0
        for i3 in c1:
            sum3+=i3.abjava + i3.abphp + i3.abhtml + i3.abqa
        repo.append(sum3)
        sum1=0
        sum2=0
        nextspr=[]
        c2 = story_details.objects.filter(sprint_id=id1)
        for i4 in c2:
            c1 = story.objects.get(id=i4.story_id)
            sum1+= i4.assigned_java_points + i4.assigned_php_points + i4.assigned_html_points + i4.assigned_qa_points
            sum2+=i4.java_points_done + i4.php_points_done + i4.html_points_done + i4.qa_points_done
            if c1.overall_status not in ['Pending Deployment','Complete','Live']:
                nextspr.append(i4.story_id)

        repo.append(sum1)
        repo.append(sum1-sum2)
        repo.append(sum2)

        list1=[]
        name = request.user.username
        xx=0
        for i in pro:
            data2 = story_details.objects.filter(sprint_id=i.id)
            list1.append([])
            l=0
            for j in data2:
                j1 = story.objects.get(sprint_id=i.id,id=j.story_id)
                list1[k].append([])
                list1[k][l].append(i.name)
                list1[k][l].append(j1.story_name)
                list1[k][l].append(j1.jira)
                if j1.overall_status==None or j1.overall_status=='':
                    list1[k][l].append('Unassigned')
                    list1[k][l].append('black')
                elif j1.overall_status in ['Blocked','Blocked on API','Blocked on HTML','Blocked on Mock','Blocked on Spec']:
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('red')
                elif j1.overall_status=='Live':
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('green')
                elif j1.overall_status=='In Progress':
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('yellow')
                elif j1.overall_status=='Next Sprint':
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('purple')
                elif j1.overall_status in ['HTML Done','PHP Done','API Done','CR']:
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('white')
                elif j1.overall_status=='QA':
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('blue')
                elif j1.overall_status in ['Pending Deployment','Complete']:
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('pd')
                else:
                    list1[k][l].append(j1.overall_status)
                    list1[k][l].append('other')
                list1[k][l].append(j1.description)
                list1[k][l].append(j.assigned_java_points + j.assigned_php_points + j.assigned_html_points + j.assigned_qa_points)
                list1[k][l].append((j.assigned_java_points + j.assigned_php_points + j.assigned_html_points + j.assigned_qa_points)-(j.java_points_done + j.php_points_done + j.html_points_done + j.qa_points_done))
                list1[k][l].append(xx)
                xx+=1
                l+=1
            k+=1

        if request.method=='GET':
            if 'sprint_name' in request.GET:
                sprname = request.GET.get('sprint_name')
                jd = request.GET.get('jira')
                skill = request.GET.get('skill')
                skill = skill.lower()
                pt = request.GET.get('points')
                if request.user.is_superuser or (user_sprint_detail.objects.filter(uname=request.user.username,sprint_id=id1,roles='man').exists()==True):
                    messages.info(request, 'Sorry authority only with Developer. Please allocate points from the story board!')
                else:
                    if skill in ['java','php','html','qa']:
                        pro = sprint.objects.get(name=sprname,project_id=pid2).id
                        st = story_details.objects.get(sprint_id=pro,jira=jd)
                        stz = story.objects.get(id=st.story_id)
                        listz=[]
                        u1 = user_detail.objects.get(uname=request.user.username)
                        if u1.java==True:
                            listz.append('java')
                        if u1.php==True:
                            listz.append('php')
                        if u1.html==True:
                            listz.append('html')
                        if u1.qa==True:
                            listz.append('qa')
                        if skill in listz:
                            stz.overall_status='In Progress'
                            if skill=='java':
                                st.dev_java=u1.name
                                st.assigned_java_points=int(pt)
                            elif skill=='php':
                                st.dev_php=u1.name
                                st.assigned_php_points=int(pt)
                            elif skill=='html':
                                st.dev_html=u1.name
                                st.assigned_html_points=int(pt)
                            elif skill=='qa':
                                st.dev_qa=u1.name
                                st.assigned_qa_points=int(pt)
                            if int(pt)>0:
                                st.save()
                            else:
                                messages.info(request, 'Unable to allocate these points! Please select valid points!')
                        else:
                            messages.info(request, 'Wrong Skill Selected! Please select from available skills provided!')
                    else:
                        messages.info(request, 'Skill Typo! Please retry!')

                return(redirect('tasks'))


        if request.method=='POST':
            if 'select_project' in request.POST:
                name1 = request.POST.get('select_project')
                proid = project.objects.get(name=name1).id
                request.session['pid'] = proid
                spr = sprint.objects.filter(project_id=proid).first()
                request.session['id'] = spr.id
                return redirect('tasks')

            if 'select_sprint' in request.POST:
                select = request.POST.get('select_sprint')
                for i in data1:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                return redirect('tasks')

            if 'move_story1' in request.POST:
                if request.user.has_perm("move_story.move_story") or ("move_story") in permission:
                    ss = request.POST.get('select_spr')
                    st1 = story.objects.filter(sprint_id=id1)
                    for i1 in st1:
                        if i1.overall_status not in ['Pending Deployment','Complete']:
                            x1 = story(sprint_id=ss,story_name=i1.story_name,description=i1.description,jira=i1.jira)
                            x1.save()
                            x2 = story.objects.latest('id')
                            x3 = story_details(sprint_id=ss,jira=x2.jira,story_id=x2.id)
                            x3.save()
                            i1.delete()
                            i1.save()
                    messages.info(request, 'Success!')
                    return redirect('tasks')
                else:
                    messages.info(request, 'UNAUTHORIZED!')
                    return redirect('tasks')

        return(render(request,'tasks.html/',{'permission':permission,'check':check,'name':name,'jd1x':jd1x,'jd2x':jd2x,'jd3x':jd3x,'listse':listse,'repo':repo,'data1':data1,'nx1':nx1,'n0':n0,'nx':nx,'list1':list1}))
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')

def home(request):
    return render(request,'home.html/',{})

def reg(request):
    total=story.objects.all().count()
    d1=User.objects.all().count()
    name=''
    email=''
    emp=0
    registered = False

    email = 'anshuman.airy@quikr.com'

    if User.objects.filter(email=email).exists() == True:
        regx = User.objects.get(email=email)
        user = authenticate(username = regx.username, password='Zehel9999')
        login(request,user)
        request.session['pid'] = 0
        request.session['user2'] = ''
        request.session['id'] = 0
        request.session['userx'] = 'Users'
        return redirect('product')

    # try:
    #     if request.method =='GET':
    #         auth_code = request.GET.get('auth_code', '')
    #         encrypt_auth = encryptx(auth_code)
    #
    #         # part2 to obtain token
    #         payload = {
    #                 'grantType':'authorization_code',
    #                 'code':encrypt_auth,
    #                 'clientId':'SprintManagement'
    #                 }
    #
    #         headers = {
    #                 'Authorization':'Basic JaA+KUfutRpIkHY54Scvn9B3XAbg3sq3enrRREIv344=',
    #                 'X-Quikr-Client':'Platform',
    #                 'Content-Type':'application/json'
    #                 }
    #
    #         response = requests.request("POST",'http://192.168.124.123:13000/identity/v1/token', data=json.dumps(payload), headers=headers)
    #         resp = response.text
    #         list1=list(map(str,resp.split('"')))
    #         idtoken = list1[5]
    #         access_token = auth_code
    #         list2=list(map(str,idtoken.split('.')))
    #         dec = decryptx(list1[5])
    #
    #         emp = int(dec['empId'])
    #         email = dec['email']
    #         name = dec['name']
    #         request.session['emp'] = emp
    #         request.session['email'] = email
    #         request.session['name'] = name
    #
    #         if User.objects.filter(email=email).exists() == True:
    #             regx = User.objects.get(email=email)
    #             user = authenticate(username = regx.username, password='Zehel9999')
    #             login(request,user)
    #             request.session['pid'] = 0
    #             request.session['user2'] = ''
    #             request.session['id'] = 0
    #             request.session['userx'] = 'Users'
    #             return redirect('product')
    # except:
    #     pass

    if request.method == 'POST':
        dev = Group.objects.get(name='Developer')
        man = Group.objects.get(name='Product Manager')
        qa = Group.objects.get(name='QA')
        user_form = UserForm(data=request.POST)
        profile_form = registerform(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            x = user.username
            profile_form.instance.uname= x
            profile = profile_form.save(commit=False)
            if ((user.email == request.session['email']) and (profile.empid == request.session['emp']) and (profile.name == request.session['name'])):
                user.set_password('Zehel9999')
                user.save()
                registered = True
                profile.user = user
                profile.save()

                z1 = user_detail.objects.latest('id')
                print(z1.roles)
                if z1.roles=='dev':
                    user.groups.add(dev)
                    user.groups.add(qa)
                else:
                    user.groups.add(man)

                return redirect('login')
            else:
                messages.info(request, 'Tampered Account Details!')
    else:
        data1 = {'email':email}
        user_form = UserForm(initial=data1)
        data2 = {'name':name,'empid':emp}
        profile_form = registerform(initial=data2)
    return render(request , 'register.html' ,{'user_form':user_form , 'profile_form':profile_form , 'registered':registered,'total':total,'d1':d1})

def admin(request):
    return redirect('http://127.0.0.1:8000/admin/')

def log(request):
    return redirect("http://192.168.124.123:13000/identity/v1/auth?auth=Basic%20JaA%2BKUfutRpIkHY54Scvn9B3XAbg3sq3enrRREIv344%3D&clientId=SprintManagement&redirectUri=http%3A%2F%2F127.0.0.1%3A8000%2F&responseType=code&scope=openid")
