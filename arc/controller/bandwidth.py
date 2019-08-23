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
    pic=''
    if display_picture.objects.filter(idx = request.user.id).exists()==True:
        pic = display_picture.objects.get(idx = request.user.id)
    else:
        pass
    per1 = Permission.objects.filter(group__user=request.user)
    for i in per1:
        permission.append(i.name)
    if request.user.has_perm("view_bandwidth.view_bandwidth") or ("view_bandwidth") in permission:
        data1 = sprint.objects.filter(project_id=pid2)
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = sprint.objects.get(id = sprid).name
        sjava = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('story_points_java'))['story_points_java__sum']
        sphp = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('story_points_php'))['story_points_php__sum']
        shtml = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('story_points_html'))['story_points_html__sum']
        sqa = user_sprint_detail.objects.filter(sprint_id=sprid).aggregate(Sum('story_points_qa'))['story_points_qa__sum']
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
                r.delta_java = r.story_points_java
            else:
                list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                r.delta_java = r.story_points_java - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
            r.save()


        list2=[]
        for i in d3:
            j = story_details.objects.filter(sprint_id=sprid, dev_php=i.name)
            r = user_sprint_detail.objects.get(roles='dev',php='True',name=i.name,sprint_id=sprid)
            if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                list2.append(0)
                r.delta_php = r.story_points_php
            else:
                list2.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                r.delta_php = r.story_points_php - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
            r.save()

        list3=[]
        for i in d4:
            j = story_details.objects.filter(sprint_id=sprid, dev_html=i.name)
            r = user_sprint_detail.objects.get(roles='dev',html='True',name=i.name,sprint_id=sprid)
            if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                list3.append(0)
                r.delta_html = r.story_points_html
            else:
                list3.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                r.delta_html = r.story_points_html - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
            r.save()

        list4=[]
        for i in d5:
            j = story_details.objects.filter(sprint_id=sprid, dev_qa=i.name)
            r = user_sprint_detail.objects.get(roles='dev',qa='True',name=i.name,sprint_id=sprid)
            if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                list4.append(0)
                r.delta_qa = r.story_points_qa
            else:
                list4.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                r.delta_qa = r.story_points_qa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
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
                        r.velocity_factor_java = vf
                        ab = (float(vf) * (p.dev_working-r.planned_leaves-r.unplanned_leaves))
                        r.available_bandwidth_java = int(ab)
                        r.story_points_java = r.available_bandwidth_java * 2
                        sjava = user_sprint_detail.objects.aggregate(Sum('story_points_java'))['story_points_java__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_java=r.name)
                        if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                            list1.append(0)
                            r.delta_java = r.story_points_java
                        else:
                            list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.delta_java = r.story_points_java - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])


                    if skill == 'php':
                        r = user_sprint_detail.objects.get(id=uid, php='True',sprint_id=sprid)
                        r.velocity_factor_php = vf
                        ab = (float(vf) * (p.dev_working-r.planned_leaves-r.unplanned_leaves))
                        r.available_bandwidth_php = int(ab)
                        r.story_points_php = r.available_bandwidth_php * 2
                        sphp = user_sprint_detail.objects.aggregate(Sum('story_points_php'))['story_points_php__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_php=r.name)
                        if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                            list1.append(0)
                            r.delta_php = r.story_points_php
                        else:
                            list1.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.delta_php = r.story_points_php - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])


                    if skill == 'html':
                        r = user_sprint_detail.objects.get(id=uid, html='True',sprint_id=sprid)
                        r.velocity_factor_html = vf
                        ab = (float(vf) * (p.dev_working-r.planned_leaves-r.unplanned_leaves))
                        r.available_bandwidth_html = int(ab)
                        r.story_points_html = r.available_bandwidth_html * 2
                        shtml = user_sprint_detail.objects.aggregate(Sum('story_points_html'))['story_points_html__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_html=r.name)
                        if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                            list1.append(0)
                            r.delta_html = r.story_points_html
                        else:
                            list1.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.delta_html = r.story_points_html - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])



                    if skill == 'qa':
                        r = user_sprint_detail.objects.get(id=uid, qa='True',sprint_id=sprid)
                        r.velocity_factor_qa = vf
                        ab = (float(vf) * (p.qa_working-r.planned_leaves-r.unplanned_leaves))
                        r.available_bandwidth_qa = int(ab)
                        r.story_points_qa = r.available_bandwidth_qa * 2
                        sqa = user_sprint_detail.objects.aggregate(Sum('story_points_qa'))['story_points_qa__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_qa=r.name)
                        if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                            list1.append(0)
                            r.delta_qa = r.story_points_qa
                        else:
                            list1.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.delta_qa = r.story_points_qa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])

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
                    r.unplanned_leaves = int(pl)
                    p = sprint.objects.get(id=sprid)
                    d2 = user_sprint_detail.objects.filter(roles='dev',java='True',sprint_id=sprid)
                    d3 = user_sprint_detail.objects.filter(roles='dev',php='True',sprint_id=sprid)
                    d4 = user_sprint_detail.objects.filter(roles='dev',html='True',sprint_id=sprid)
                    d5 = user_sprint_detail.objects.filter(roles='dev',qa='True',sprint_id=sprid)
                    r.save()

                    if skill=='java':
                        r = user_sprint_detail.objects.get(id=uid,java='True',sprint_id=sprid)
                        ab = (r.velocity_factor_java)*(p.dev_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_java=ab
                        r.story_points_java = r.available_bandwidth_java * 2
                        sjava = user_sprint_detail.objects.aggregate(Sum('story_points_java'))['story_points_java__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_java=r.name)
                        if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                            list1.append(0)
                            r.delta_java = r.story_points_java
                        else:
                            list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.delta_java = r.story_points_java - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])

                            r.save()


                    if skill=='php':
                        r = user_sprint_detail.objects.get(id=uid,php='True',sprint_id=sprid)
                        ab = (r.velocity_factor_php)*(p.dev_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_php=ab
                        r.story_points_php = r.available_bandwidth_php * 2
                        sphp = user_sprint_detail.objects.aggregate(Sum('story_points_php'))['story_points_php__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_php=r.name)
                        if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                            list1.append(0)
                            r.delta_php = r.story_points_php
                        else:
                            list1.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.delta_php = r.story_points_php - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.save()


                    if skill=='html':
                        r = user_sprint_detail.objects.get(id=uid,html='True',sprint_id=sprid)
                        ab = (r.velocity_factor_html)*(p.dev_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_html=ab
                        r.story_points_html = r.available_bandwidth_html * 2
                        shtml = user_sprint_detail.objects.aggregate(Sum('story_points_html'))['story_points_html__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_html=r.name)
                        if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                            list1.append(0)
                            r.delta_html = r.story_points_html
                        else:
                            list1.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.delta_html = r.story_points_html - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.save()

                    if skill=='qa':
                        r = user_sprint_detail.objects.get(id=uid,qa='True',sprint_id=sprid)
                        ab = (r.velocity_factor_qa)*(p.qa_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_qa=ab
                        r.story_points_qa = r.available_bandwidth_qa * 2
                        sqa = user_sprint_detail.objects.aggregate(Sum('story_points_qa'))['story_points_qa__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_qa=r.name)
                        if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                            list1.append(0)
                            r.delta_qa = r.story_points_qa
                        else:
                            list1.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.delta_qa = r.story_points_qa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
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
                    r.planned_leaves = int(pl)
                    p = sprint.objects.get(id=sprid)
                    d2 = user_sprint_detail.objects.filter(roles='dev',java='True',sprint_id=sprid)
                    d3 = user_sprint_detail.objects.filter(roles='dev',php='True',sprint_id=sprid)
                    d4 = user_sprint_detail.objects.filter(roles='dev',html='True',sprint_id=sprid)
                    d5 = user_sprint_detail.objects.filter(roles='dev',qa='True',sprint_id=sprid)
                    r.save()

                    if skill=='java':
                        r = user_sprint_detail.objects.get(id=uid,java='True',sprint_id=sprid)
                        ab = (r.velocity_factor_java)*(p.dev_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_java=ab
                        r.story_points_java = r.available_bandwidth_java * 2
                        sjava = user_sprint_detail.objects.aggregate(Sum('story_points_java'))['story_points_java__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_java=r.name)
                        if j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'] == None:
                            list1.append(0)
                            r.delta_java = r.story_points_java
                        else:
                            list1.append(j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.delta_java = r.story_points_java - (j.aggregate(Sum('assigned_java_points'))['assigned_java_points__sum'])
                            r.save()


                    if skill=='php':
                        r = user_sprint_detail.objects.get(id=uid,php='True',sprint_id=sprid)
                        ab = (r.velocity_factor_php)*(p.dev_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_php=ab
                        r.story_points_php = r.available_bandwidth_php * 2
                        sphp = user_sprint_detail.objects.aggregate(Sum('story_points_php'))['story_points_php__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_php=r.name)
                        if j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'] == None:
                            list1.append(0)
                            r.delta_php = r.story_points_php
                        else:
                            list1.append(j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.delta_php = r.story_points_php - (j.aggregate(Sum('assigned_php_points'))['assigned_php_points__sum'])
                            r.save()


                    if skill=='html':
                        r = user_sprint_detail.objects.get(id=uid,html='True',sprint_id=sprid)
                        ab = (r.velocity_factor_html)*(p.dev_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_html=ab
                        r.story_points_html = r.available_bandwidth_html * 2
                        shtml = user_sprint_detail.objects.aggregate(Sum('story_points_html'))['story_points_html__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_html=r.name)
                        if j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'] == None:
                            list1.append(0)
                            r.delta_html = r.story_points_html
                        else:
                            list1.append(j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.delta_html = r.story_points_html - (j.aggregate(Sum('assigned_html_points'))['assigned_html_points__sum'])
                            r.save()

                    if skill=='qa':
                        r = user_sprint_detail.objects.get(id=uid,qa='True',sprint_id=sprid)
                        ab = (r.velocity_factor_qa)*(p.qa_working-r.planned_leaves-r.unplanned_leaves)
                        r.available_bandwidth_qa=ab
                        r.story_points_qa = r.available_bandwidth_qa * 2
                        sqa = user_sprint_detail.objects.aggregate(Sum('story_points_qa'))['story_points_qa__sum']
                        j = story_details.objects.filter(sprint_id=sprid, dev_qa=r.name)
                        if j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'] == None:
                            list1.append(0)
                            r.delta_qa = r.story_points_qa
                        else:
                            list1.append(j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
                            r.delta_qa = r.story_points_qa - (j.aggregate(Sum('assigned_qa_points'))['assigned_qa_points__sum'])
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

        return(render(request,'bandwidth.html/',{'pic':pic,'permission':permission,'name':name,'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'band':band,'d1':d1,'data':data,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'list1':list1,'list2':list2,'list3':list3,'list4':list4}))
    else:
        messages.info(request, 'You are unauthorized to view this page! Redirecting to home page.')
        return redirect('product')
