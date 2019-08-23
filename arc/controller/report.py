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
    pic=''
    if display_picture.objects.filter(idx = request.user.id).exists()==True:
        pic = display_picture.objects.get(idx = request.user.id)
    else:
        pass
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
            sum3+=i3.available_bandwidth_java + i3.available_bandwidth_php + i3.available_bandwidth_html + i3.available_bandwidth_qa
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
                list1[k][l].append(j1.id)
                xx+=1
                l+=1
            k+=1

        if request.method=='GET':
            if 'red' in request.GET:
                idx = request.GET.get('red')
                request.session['story_id'] = idx
                return(redirect('story'))

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
                        st = story_details.objects.filter(sprint_id=pro,jira=jd).latest('id')
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

        return(render(request,'tasks.html/',{'pic':pic,'permission':permission,'check':check,'name':name,'jd1x':jd1x,'jd2x':jd2x,'jd3x':jd3x,'listse':listse,'repo':repo,'data1':data1,'nx1':nx1,'n0':n0,'nx':nx,'list1':list1}))
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')
