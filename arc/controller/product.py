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
    pic=''
    if display_picture.objects.filter(idx = request.user.id).exists()==True:
        pic = display_picture.objects.get(idx = request.user.id)
    else:
        pass
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
    z=0
    counter = 0
    left2=0
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
            p2 = progress.objects.filter(work_date=dt.strftime("%Y-%m-%d")).exclude(status='')
            s2=0
            s3=0
            s4=0
            s6=0
            s7=0
            jira=''
            for i2 in p2:
                if story_details.objects.filter(sprint_id=id,jira=i2.jira_id).exists()==True:
                #     counter=counter+1
                    s5 = story_details.objects.filter(sprint_id=id,jira=i2.jira_id).latest('id')
                    if i2.jira_id != jira:
                        if s5.dev_java==i2.dev_name:
                            s4+=s5.assigned_java_points
                        elif s5.dev_php==i2.dev_name:
                            s4+=s5.assigned_php_points
                        elif s5.dev_html==i2.dev_name:
                            s4+=s5.assigned_html_points
                        elif s5.dev_qa==i2.dev_name:
                            s4+=s5.assigned_qa_points
                        jira = i2.jira_id

                    s2+=i2.actual
                    if i2.left != i2.calculated_left and (abs(i2.left-left2)!=i2.actual):
                        s3+=i2.left
                        # sum2=sum2-i2.actual
                        if (i2.calculated_left-i2.left)>0:
                            sum2=sum2-i2.actual-(i2.calculated_left-i2.left)
                            left2 = i2.left
                        else:
                            sum2=sum2-i2.actual+(i2.calculated_left-i2.left)
                            left2 = i2.left
                    else:
                        s3+=i2.calculated_left
                        sum2=sum2-i2.actual
                        left2 = i2.left
                    # s3+=i2.left
                    # s6+=i2.calculated_left
                    # s7=i2.left
            list5.append(sum2)
            if (cal+1)!=0:
                sumx-=(sumy/(cal+1))
                list6.append(sumx)
            # print(list5)

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
        ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
            ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
            ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
            ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
            ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
            ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
                ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
                    ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
                    ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
                    ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
                    ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
                    ab = s2.story_points_java + s2.story_points_php + s2.story_points_html +s2.story_points_qa
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
                    print(selected_mans)
                    print(selected_users)
                    for i1 in x1:
                        if i1.uname in selected_mans:
                            x2 = user_sprint_detail(sprint_id=x,uname=i1.uname,name=i1.name,roles='man',java=i1.java,html=i1.html,php=i1.php,qa=i1.php)
                            if request.user.has_perm("add_sprint.add_sprint") or ("add_sprint") in permission:
                                x2.save()
                                print(i1.uname,'man')
                            else:
                                messages.info(request, 'UNAUTHORIZED!')
                                return redirect('product')
                        elif i1.uname in selected_users:
                            x2 = user_sprint_detail(sprint_id=x,uname=i1.uname,name=i1.name,roles='dev',java=i1.java,html=i1.html,php=i1.php,qa=i1.php)
                            if request.user.has_perm("add_sprint.add_sprint") or ("add_sprint") in permission:
                                x2.save()
                                print(i1.uname,'dev')
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

    return(render(request,'product.html/',context={'pic':pic,'permission':permission,'name':name,'z2':z2,'nval':nval,'val':val,'hx2':hx2,'hx1':hx1,'jd8':jd8,'s22':s22,'jd7':jd7,'jd6':jd6,'jd5':jd5,'jd1':jd1,'form':form,'data':data,'n':n,'nx':nx,'list11':list11}))
