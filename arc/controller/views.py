from django.shortcuts import render,redirect
from arc.forms.register_forms import registerform,UserForm
from arc.forms.prod_forms import productform
from arc.forms.story_forms import storyform
from arc.models.register_mod import register
from arc.models.project_mod import project
from arc.models.story_mod import story
from arc.models.prod_mod import product
from arc.models.prg_mod import prg
from arc.models.reg_mod import cregister
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
from datetime import datetime
import numpy as np
import json
import csv, io

def checkman(user):
    if user.is_superuser:
        return(True)
    else:
        if register.objects.get(uname=user.username).roles=='man':
            return True

def check(user):
    if user.is_superuser:
        return (0)
    else:
        if register.objects.get(uname=user.username).roles=='man':
            return (0)
        else:
            return(1)

@login_required
def qaprg(request):
    if check(request.user)==0:
        id1 = request.session['id']
        pid2 = request.session['pid']
        data1 = product.objects.filter(pid=pid2)
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = product.objects.get(id = id1).name
        data = cregister.objects.filter(roles='dev',sprint_id=id1)
        list1=[]
        j=0
        p = product.objects.get(id=id1)
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
            st1 = story.objects.filter(sprint_id=id1,dev_java=i1.name) | story.objects.filter(sprint_id=id1,dev_php=i1.name) | story.objects.filter(sprint_id=id1,dev_html=i1.name) | story.objects.filter(sprint_id=id1,dev_qa=i1.name)
            list2[i1.name]={}
            for j1 in st1:
                if prg.objects.filter(s_id=id1,jd=j1.jira,dname=i1.name).exists()==True:
                    p1 = prg.objects.filter(s_id=id1,jd=j1.jira,dname=i1.name)
                    list2[i1.name][n]={}
                    for k1 in p1:
                        list2[i1.name][n][str(k1.sdate)]=str(k1.sdate)
                    n+=1
                else:
                    n+=1
        jd1=json.dumps(list2)

        list3={}
        n=0
        for i2 in data:
            st1 = story.objects.filter(sprint_id=id1,dev_java=i2.name) | story.objects.filter(sprint_id=id1,dev_php=i2.name) | story.objects.filter(sprint_id=id1,dev_html=i2.name) | story.objects.filter(sprint_id=id1,dev_qa=i2.name)
            list3[i2.name]={}
            for j2 in st1:
                if prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name).exists()==True:
                    r=0
                    p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name)
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
            st1 = story.objects.filter(sprint_id=id1,dev_java=i2.name) | story.objects.filter(sprint_id=id1,dev_php=i2.name) | story.objects.filter(sprint_id=id1,dev_html=i2.name) | story.objects.filter(sprint_id=id1,dev_qa=i2.name)
            list4[i2.name]={}
            for j2 in st1:
                if prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name).exists()==True:
                    p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name)
                    for k2 in p1:
                        list4[i2.name][n]=k2.jd
                        n+=1
                else:
                    n+=1
        jd3=json.dumps(list4)

        count=0
        for i in data:
            list1.append([])
            k=0
            st = story.objects.filter(sprint_id=id1,dev_java=i.name) | story.objects.filter(sprint_id=id1,dev_php=i.name) | story.objects.filter(sprint_id=id1,dev_html=i.name) | story.objects.filter(sprint_id=id1,dev_qa=i.name)
            for r in st:
                list1[j].append([])
                list1[j][k].append(r.story_name)
                list1[j][k].append(r.jira)
                if r.dev_java==i.name:
                    list1[j][k].append(r.javas)
                    list1[j][k].append(r.ostatus)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r.jactual)
                elif r.dev_php==i.name:
                    list1[j][k].append(r.phps)
                    list1[j][k].append(r.ostatus)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r.pactual)
                elif r.dev_html==i.name:
                    list1[j][k].append(r.htmls)
                    list1[j][k].append(r.ostatus)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r.hactual)
                elif r.dev_qa==i.name:
                    list1[j][k].append(r.qas)
                    list1[j][k].append(r.ostatus)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r.qactual)
                k+=1
                count=count+1;
            j+=1
        # print(list1)

        if request.method=='GET':
            if 'as' in request.GET:
                s = request.GET.get('sel')
                j = request.GET.get('jid')
                n1 = request.GET.get('name1')
                p = story.objects.get(sprint_id=id1,jira = j)
                p.ostatus=s
                p.save()
                print(p.ostatus)
                return redirect('qaprg')

            if 'as1' in request.GET:
                stdate = request.GET.get('startdate')
                prog = request.GET.get('prg')
                j = request.GET.get('j1')
                n2 = request.GET.get('name2')
                frac = request.GET.get('fraction')
                frac1=0
                if frac=='Quarter Day':
                    frac1=.5
                elif frac=='Half Day':
                    frac1=1
                elif frac=='Three Quarters Day':
                    frac1=1.5
                else:
                    frac1=2
                st = story.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                for ix in st:
                    if ix.dev_java==n2:
                        ix.jactual = ix.jactual + frac1
                    elif ix.dev_php==n2:
                        ix.pactual = ix.pactual + frac1
                    elif ix.dev_html==n2:
                        ix.hactual = ix.hactual + frac1
                    else:
                        ix.qactual = ix.qactual + frac1
                    ix.save()
                z = prg(s_id=id1,jd=j,sdate=stdate,status=prog,dname=n2)
                z.save()


                list2={}
                for i1 in data:
                    st1 = story.objects.filter(sprint_id=id1,dev_java=i1.name) | story.objects.filter(sprint_id=id1,dev_php=i1.name) | story.objects.filter(sprint_id=id1,dev_html=i1.name) | story.objects.filter(sprint_id=id1,dev_qa=i1.name)
                    n=0
                    list2[i1.name]={}
                    for j1 in st1:
                        if prg.objects.filter(s_id=id1,jd=j1.jira,dname=i1.name).exists()==True:
                            p1 = prg.objects.filter(s_id=id1,jd=j1.jira,dname=i1.name)
                            for k1 in p1:
                                list2[i1.name][n]={}
                                list2[i1.name][n][str(k1.sdate)]=str(k1.sdate)
                                n+=1

                jd1=json.dumps(list2)

                list3={}
                m=0
                for i2 in data:
                    st1 = story.objects.filter(sprint_id=id1,dev_java=i2.name) | story.objects.filter(sprint_id=id1,dev_php=i2.name) | story.objects.filter(sprint_id=id1,dev_html=i2.name) | story.objects.filter(sprint_id=id1,dev_qa=i2.name)
                    n=0
                    list3[m]={}
                    for j2 in st1:
                        if prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name).exists()==True:
                            p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name)
                            for k2 in p1:
                                list3[m][n]=k2.status
                                n+=1
                    m+=1
                jd2=json.dumps(list3)

                list4={}
                m=0
                for i2 in data:
                    st1 = story.objects.filter(sprint_id=id1,dev_java=i2.name) | story.objects.filter(sprint_id=id1,dev_php=i2.name) | story.objects.filter(sprint_id=id1,dev_html=i2.name) | story.objects.filter(sprint_id=id1,dev_qa=i2.name)
                    n=0
                    list4[m]={}
                    for j2 in st1:
                        if prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name).exists()==True:
                            p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name)
                            for k2 in p1:
                                list4[m][n]=k2.jd
                                n+=1
                    m+=1
                jd3=json.dumps(list4)
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
                return redirect('qaprg')


    else:

        id1 = request.session['id']
        pid2 = request.session['pid']
        data1 = product.objects.filter(pid=pid2)
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = product.objects.get(id = id1).name
        list1=[]
        j=0
        p = product.objects.get(id=id1)
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
        name1 = register.objects.get(uname=x).name
        data = cregister.objects.filter(roles='dev',name=name1,sprint_id=id1)

        list2={}
        n=0
        for i1 in data:
            st1 = story.objects.filter(sprint_id=id1,dev_java=name1) | story.objects.filter(sprint_id=id1,dev_php=name1) | story.objects.filter(sprint_id=id1,dev_html=name1) | story.objects.filter(sprint_id=id1,dev_qa=name1)
            list2[name1]={}
            for j1 in st1:
                if prg.objects.filter(s_id=id1,jd=j1.jira,dname=name1).exists()==True:
                    p1 = prg.objects.filter(s_id=id1,jd=j1.jira,dname=name1)
                    list2[name1][n]={}
                    for k1 in p1:
                        list2[name1][n][str(k1.sdate)]=str(k1.sdate)
                    n+=1
                else:
                    n+=1
        jd1=json.dumps(list2)
        # print(list2)

        list3={}
        n=0
        st1 = story.objects.filter(sprint_id=id1,dev_java=name1) | story.objects.filter(sprint_id=id1,dev_php=name1) | story.objects.filter(sprint_id=id1,dev_html=name1) | story.objects.filter(sprint_id=id1,dev_qa=name1)
        list3[name1]={}
        for j2 in st1:
            if prg.objects.filter(s_id=id1,jd=j2.jira,dname=name1).exists()==True:
                r=0
                p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=name1)
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
        st1 = story.objects.filter(sprint_id=id1,dev_java=name1) | story.objects.filter(sprint_id=id1,dev_php=name1) | story.objects.filter(sprint_id=id1,dev_html=name1) | story.objects.filter(sprint_id=id1,dev_qa=name1)
        list4[name1]={}
        for j2 in st1:
            if prg.objects.filter(s_id=id1,jd=j2.jira,dname=name1).exists()==True:
                p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=name1)
                for k2 in p1:
                    list4[name1][n]=k2.jd
                    n+=1
            else:
                n+=1
        jd3=json.dumps(list4)

        count=0
        list1.append([])
        k=0
        st = story.objects.filter(sprint_id=id1,dev_java=name1) | story.objects.filter(sprint_id=id1,dev_php=name1) | story.objects.filter(sprint_id=id1,dev_html=name1) | story.objects.filter(sprint_id=id1,dev_qa=name1)
        for r in st:
            list1[j].append([])
            list1[j][k].append(r.story_name)
            list1[j][k].append(r.jira)
            if r.dev_java==name1:
                list1[j][k].append(r.javas)
                list1[j][k].append(r.ostatus)
                list1[j][k].append(name1)
                list1[j][k].append(count)
            elif r.dev_php==name1:
                list1[j][k].append(r.phps)
                list1[j][k].append(r.ostatus)
                list1[j][k].append(name1)
                list1[j][k].append(count)
            elif r.dev_html==name1:
                list1[j][k].append(r.htmls)
                list1[j][k].append(r.ostatus)
                list1[j][k].append(name1)
                list1[j][k].append(count)
            elif r.dev_qa==name1:
                list1[j][k].append(r.qas)
                list1[j][k].append(r.ostatus)
                list1[j][k].append(name1)
                list1[j][k].append(count)
            listb=[]
            if prg.objects.filter(s_id=id1,jd=r.jira,dname=name1).exists()==True:
                p1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=name1)
                for k1 in p1:
                    listb.append(k1.sdate)
                    listb=list(set(listb))
                list1[j][k].append(len(listb)*2)
            else:
                list1[j][k].append(0)
            k+=1
            count=count+1;
        j+=1

        if request.method=='GET':
            if 'as' in request.GET:
                s = request.GET.get('sel')
                j = request.GET.get('jid')
                n1 = request.GET.get('name1')
                p = story.objects.get(sprint_id=id1,jira = j)
                p.ostatus=s
                p.save()
                return redirect('qaprg')

            if 'startdate' in request.GET:
                stdate = request.GET.get('startdate')
                prog = request.GET.get('prg')
                j = request.GET.get('j1')
                n2 = request.GET.get('name2')
                st = story.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                z = prg(s_id=id1,jd=j,sdate=stdate,status=prog,dname=n2)
                z.save()

                list2={}
                for i1 in data:
                    st1 = story.objects.filter(sprint_id=id1,dev_java=i1.name) | story.objects.filter(sprint_id=id1,dev_php=i1.name) | story.objects.filter(sprint_id=id1,dev_html=i1.name) | story.objects.filter(sprint_id=id1,dev_qa=i1.name)
                    n=0
                    list2[i1.name]={}
                    for j1 in st1:
                        if prg.objects.filter(s_id=id1,jd=j1.jira,dname=i1.name).exists()==True:
                            p1 = prg.objects.filter(s_id=id1,jd=j1.jira,dname=i1.name)
                            for k1 in p1:
                                list2[i1.name][n]={}
                                list2[i1.name][n][str(k1.sdate)]=str(k1.sdate)
                                n+=1

                jd1=json.dumps(list2)

                list3={}
                m=0
                for i2 in data:
                    st1 = story.objects.filter(sprint_id=id1,dev_java=i2.name) | story.objects.filter(sprint_id=id1,dev_php=i2.name) | story.objects.filter(sprint_id=id1,dev_html=i2.name) | story.objects.filter(sprint_id=id1,dev_qa=i2.name)
                    n=0
                    list3[m]={}
                    for j2 in st1:
                        if prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name).exists()==True:
                            p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name)
                            for k2 in p1:
                                list3[m][n]=k2.status
                                n+=1
                    m+=1
                jd2=json.dumps(list3)

                list4={}
                m=0
                for i2 in data:
                    st1 = story.objects.filter(sprint_id=id1,dev_java=i2.name) | story.objects.filter(sprint_id=id1,dev_php=i2.name) | story.objects.filter(sprint_id=id1,dev_html=i2.name) | story.objects.filter(sprint_id=id1,dev_qa=i2.name)
                    n=0
                    list4[m]={}
                    for j2 in st1:
                        if prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name).exists()==True:
                            p1 = prg.objects.filter(s_id=id1,jd=j2.jira,dname=i2.name)
                            for k2 in p1:
                                list4[m][n]=k2.jd
                                n+=1
                    m+=1
                jd3=json.dumps(list4)
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
                return redirect('qaprg')

    return(render(request,'qaprg.html/',{'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'data':data,'list1':list1,'p':p,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'d1':jd1,'d2':jd2,'d3':jd3}))

@login_required
def user_logout(request):
    logout(request)
    return redirect('login.html/')


@login_required
def prod(request):
    pid2 = request.session['pid']
    data = product.objects.filter(pid=pid2)
    n = project.objects.all().exclude(id=0)
    nx = project.objects.get(id=pid2)
    form = productform(request.POST or None)
    list11=[]
    z1 = User.objects.all()
    for i11 in z1:
        if i11.is_superuser:
            list11.append(i11.username)

    if request.method=='POST':
        # productform condition where sprint_button is the name for submit button for sprint form
        if 'sprint_button' in request.POST:
            if request.user.is_superuser or register.objects.get(uname=request.user.username).roles=='man':
                if form.is_valid():
                    form = productform(request.POST)
                    form.instance.pid = pid2
                    form.save()
                    x = form.instance.id
                    x1 = register.objects.all()
                    for i1 in x1:
                        x2 = cregister(sprint_id=x,uname=i1.uname,name=i1.name,roles=i1.roles,java=i1.java,html=i1.html,php=i1.php,qa=i1.php)
                        x2.save()
                    return redirect('product')
                else:
                    return HttpResponse("Data not stored!")
            else:
                return HttpResponse('You are not Authorized')
        #select sprint get value and redirect
        if 'submit_sprint' in request.POST:
            select = request.POST.get('select_sprint')
            if select==None:
                return HttpResponse('Please select a Valid Sprint!')
            else:
                for i in data:
                    if select in i.name:
                        id=i.id
                        request.session['id'] = id
                        break
                if request.user.is_superuser:
                    return redirect('view_story')
                else:
                    if register.objects.get(uname=request.user.username).roles=='dev':
                        return redirect('qaprg')
                    else:
                        return redirect('view_story')

        if 'project_button' in request.POST:
            name1 = request.POST.get('pname')
            user1 = request.POST.get('select_admin')
            n = project.objects.all().exclude(id=0)
            a=0
            if request.user.is_superuser and request.user.username == user1:
                for i in n:
                    if name1==i.name:
                        a+=1
                        return HttpResponse("Project Name already taken. Please Choose another one!")
                if a==0:
                    z = project(name = name1)
                    z.save()
            else:
                return HttpResponse('You are not Authorized!')

            return(redirect('product'))

        if 'select_project' in request.POST:
            name1 = request.POST.get('select_project')
            proid = project.objects.get(name=name1).id
            if proid==0:
                return HttpResponse('Please choose a valid Project!')
            else:
                request.session['pid'] = proid
            return(redirect('product'))

    else:
        form = productform()
    return(render(request,'product.html/',context={'form':form,'data':data,'n':n,'nx':nx,'list11':list11}))

@login_required
@user_passes_test(checkman,login_url='progress')
def view_story(request):
    id = request.session['id']
    pid2 = request.session['pid']
    data1 = product.objects.filter(pid=pid2)
    n = project.objects.all().exclude(id=0)
    nx = project.objects.get(id=pid2)
    nx1 = product.objects.get(id = id).name
    data = story.objects.filter(sprint_id=id)
    form = storyform(request.POST or None)
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    for i in data:
        list1.append(i.id)
        list2.append(i.story_name)
        list3.append(i.description)
        list4.append(i.jira)
    jd1=json.dumps(list1)
    jd2=json.dumps(list2)
    jd3=json.dumps(list3)
    jd4=json.dumps(list4)

    if request.method=='GET':
        if 'delete_story' in request.GET:
            x = request.GET.get('delete_story')
            story.objects.filter(sprint_id=id,id=x).delete()
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
            p.save()
            return(redirect('view_story'))

    if request.method=='POST':
        if 'submit_sprint' in request.POST:
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
            return redirect('view_story')

        if 'csv_button' in request.POST:
            csv_file = request.FILES['file1']
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('Not a CSV File!')
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
                        # print(fields)
                        stx = story.objects.filter(sprint_id=id)
                        l=0
                        for i in stx:
                            if fields[2]==i.jira:
                                l+=1
                        if l==0:
                            k=0
                            for i3 in register.objects.all():
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
                            if fields[10] in ['Live','In Progress','HTML Done','PHP Done','API Done','QA','Pending Development','Blocked','Blocked on API','Blocked on HTML','Blocked on Mock','Blocked on Spec','Not Needed','Next Sprint','Duplicate','CR','',' ']:
                                k+=1
                            if k==5:
                                for i2 in range(4,11,2):
                                    if fields[i2] in ['null', 'None', '','None ',' ']:
                                        fields[i2] = 0
                                    if int(fields[i2])<0:
                                        fields[i2] = 0
                                z1 = story(sprint_id=id,story_name=fields[0],description=fields[1],jira=fields[2],dev_java=fields[3],javas=int(fields[4]),dev_php=fields[5],phps=int(fields[6]),dev_html=fields[7],htmls=int(fields[8]),dev_qa=fields[9],qas=int(fields[10]),ostatus=fields[11])
                                z1.save()
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
                        return HttpResponse("Jira ID already exists! Please Choose another one!")
                form.save()
                return redirect('view_story')
            else:
                return HttpResponse("Data not stored!")
        else:
            form = storyform()

    return render(request,'view_story.html/',{'form':form,'data':data,'jd1':jd1,'jd2':jd2,'jd3':jd3,'jd4':jd4,'n':n,'nx':nx,'data1':data1,'nx1':nx1})

@login_required
@user_passes_test(checkman,login_url='progress')
def bandwidth(request):
    sprid = request.session['id']
    pid2 = request.session['pid']
    data1 = product.objects.filter(pid=pid2)
    n0 = project.objects.all().exclude(id=0)
    nx = project.objects.get(id=pid2)
    nx1 = product.objects.get(id = sprid).name
    sjava = cregister.objects.filter(sprint_id=sprid).aggregate(Sum('spjava'))['spjava__sum']
    sphp = cregister.objects.filter(sprint_id=sprid).aggregate(Sum('spphp'))['spphp__sum']
    shtml = cregister.objects.filter(sprint_id=sprid).aggregate(Sum('sphtml'))['sphtml__sum']
    sqa = cregister.objects.filter(sprint_id=sprid).aggregate(Sum('spqa'))['spqa__sum']
    band = product.objects.filter(id=sprid)
    data = story.objects.filter(sprint_id=sprid)
    d1 = cregister.objects.filter(roles='dev')
    d2 = cregister.objects.filter(roles='dev',java='True',sprint_id=sprid)
    d3 = cregister.objects.filter(roles='dev',php='True',sprint_id=sprid)
    d4 = cregister.objects.filter(roles='dev',html='True',sprint_id=sprid)
    d5 = cregister.objects.filter(roles='dev',qa='True',sprint_id=sprid)

    list1=[]
    for i in d2:
        j = story.objects.filter(sprint_id=sprid, dev_java=i.name)
        r = cregister.objects.get(roles='dev',java='True',name=i.name,sprint_id=sprid)
        if j.aggregate(Sum('javas'))['javas__sum'] == None:
            list1.append(0)
            r.djava = r.spjava
        else:
            list1.append(j.aggregate(Sum('javas'))['javas__sum'])
            r.djava = r.spjava - (j.aggregate(Sum('javas'))['javas__sum'])
        r.save()


    list2=[]
    for i in d3:
        j = story.objects.filter(sprint_id=sprid, dev_php=i.name)
        r = cregister.objects.get(roles='dev',php='True',name=i.name,sprint_id=sprid)
        if j.aggregate(Sum('phps'))['phps__sum'] == None:
            list2.append(0)
            r.dphp = r.spphp
        else:
            list2.append(j.aggregate(Sum('phps'))['phps__sum'])
            r.dphp = r.spphp - (j.aggregate(Sum('phps'))['phps__sum'])
        r.save()

    list3=[]
    for i in d4:
        j = story.objects.filter(sprint_id=sprid, dev_html=i.name)
        r = cregister.objects.get(roles='dev',html='True',name=i.name,sprint_id=sprid)
        if j.aggregate(Sum('htmls'))['htmls__sum'] == None:
            list3.append(0)
            r.dhtml = r.sphtml
        else:
            list3.append(j.aggregate(Sum('htmls'))['htmls__sum'])
            r.dhtml = r.sphtml - (j.aggregate(Sum('htmls'))['htmls__sum'])
        r.save()

    list4=[]
    for i in d5:
        j = story.objects.filter(sprint_id=sprid, dev_qa=i.name)
        r = cregister.objects.get(roles='dev',qa='True',name=i.name,sprint_id=sprid)
        if j.aggregate(Sum('qas'))['qas__sum'] == None:
            list4.append(0)
            r.dqa = r.spqa
        else:
            list4.append(j.aggregate(Sum('qas'))['qas__sum'])
            r.dqa = r.spqa - (j.aggregate(Sum('qas'))['qas__sum'])
        r.save()

    x = product.objects.get(id=sprid)
    day1 = (x.sprint_start_date + timedelta(x1 + 1) for x1 in range((x.sprint_dev_end_date - x.sprint_start_date).days))
    y = sum(1 for day in day1 if day.weekday() < 5)

    day2 = (x.sprint_start_date + timedelta(x1 + 1) for x1 in range((x.sprint_qa_end_date - x.sprint_start_date).days))
    z = sum(1 for day in day2 if day.weekday() < 5)

    y = y - x.holidays
    z = z - x.holidays
    x.dev_working = y
    x.qa_working = z
    x.save()

    if request.method=='GET':
        if 'assign1' in request.GET:
            vf = request.GET.get('assign1')
            uid = request.GET.get('assign2')
            skill = request.GET.get('assign3')
            p = product.objects.get(id=sprid)

            if skill == 'java':
                r = cregister.objects.get(id=uid, java='True',sprint_id=sprid)
                r.vfjava = vf
                ab = (float(vf) * (p.dev_working-r.planned-r.unplanned))
                r.abjava = int(ab)
                r.spjava = r.abjava * 2
                sjava = cregister.objects.aggregate(Sum('spjava'))['spjava__sum']
                j = story.objects.filter(sprint_id=sprid, dev_java=r.name)
                if j.aggregate(Sum('javas'))['javas__sum'] == None:
                    list1.append(0)
                    r.djava = r.spjava
                else:
                    list1.append(j.aggregate(Sum('javas'))['javas__sum'])
                    r.djava = r.spjava - (j.aggregate(Sum('javas'))['javas__sum'])


            if skill == 'php':
                r = cregister.objects.get(id=uid, php='True',sprint_id=sprid)
                r.vfphp = vf
                ab = (float(vf) * (p.dev_working-r.planned-r.unplanned))
                r.abphp = int(ab)
                r.spphp = r.abphp * 2
                sphp = cregister.objects.aggregate(Sum('spphp'))['spphp__sum']
                j = story.objects.filter(sprint_id=sprid, dev_php=r.name)
                if j.aggregate(Sum('phps'))['phps__sum'] == None:
                    list1.append(0)
                    r.dphp = r.spphp
                else:
                    list1.append(j.aggregate(Sum('phps'))['phps__sum'])
                    r.dphp = r.spphp - (j.aggregate(Sum('phps'))['phps__sum'])


            if skill == 'html':
                r = cregister.objects.get(id=uid, html='True',sprint_id=sprid)
                r.vfhtml = vf
                ab = (float(vf) * (p.dev_working-r.planned-r.unplanned))
                r.abhtml = int(ab)
                r.sphtml = r.abhtml * 2
                shtml = cregister.objects.aggregate(Sum('sphtml'))['sphtml__sum']
                j = story.objects.filter(sprint_id=sprid, dev_html=r.name)
                if j.aggregate(Sum('htmls'))['htmls__sum'] == None:
                    list1.append(0)
                    r.dhtml = r.sphtml
                else:
                    list1.append(j.aggregate(Sum('htmls'))['htmls__sum'])
                    r.dhtml = r.sphtml - (j.aggregate(Sum('htmls'))['htmls__sum'])



            if skill == 'qa':
                r = cregister.objects.get(id=uid, qa='True',sprint_id=sprid)
                r.vfqa = vf
                ab = (float(vf) * (p.qa_working-r.planned-r.unplanned))
                r.abqa = int(ab)
                r.spqa = r.abqa * 2
                sqa = cregister.objects.aggregate(Sum('spqa'))['spqa__sum']
                j = story.objects.filter(sprint_id=sprid, dev_qa=r.name)
                if j.aggregate(Sum('qas'))['qas__sum'] == None:
                    list1.append(0)
                    r.dqa = r.spqa
                else:
                    list1.append(j.aggregate(Sum('qas'))['qas__sum'])
                    r.dqa = r.spqa - (j.aggregate(Sum('qas'))['qas__sum'])

            r.save()
            return redirect('/bandwidth/')


        if 'uleave1' in request.GET:
            pl = request.GET.get('uleave1')
            uid = request.GET.get('uleave2')
            skill = request.GET.get('uleave3')
            r = cregister.objects.get(id=uid,sprint_id=sprid)
            r.unplanned = int(pl)
            p = product.objects.get(id=sprid)
            d2 = cregister.objects.filter(roles='dev',java='True',sprint_id=sprid)
            d3 = cregister.objects.filter(roles='dev',php='True',sprint_id=sprid)
            d4 = cregister.objects.filter(roles='dev',html='True',sprint_id=sprid)
            d5 = cregister.objects.filter(roles='dev',qa='True',sprint_id=sprid)
            r.save()

            if skill=='java':
                r = cregister.objects.get(id=uid,java='True',sprint_id=sprid)
                ab = (r.vfjava)*(p.dev_working-r.planned-r.unplanned)
                r.abjava=ab
                r.spjava = r.abjava * 2
                sjava = cregister.objects.aggregate(Sum('spjava'))['spjava__sum']
                j = story.objects.filter(sprint_id=sprid, dev_java=r.name)
                if j.aggregate(Sum('javas'))['javas__sum'] == None:
                    list1.append(0)
                    r.djava = r.spjava
                else:
                    list1.append(j.aggregate(Sum('javas'))['javas__sum'])
                    r.djava = r.spjava - (j.aggregate(Sum('javas'))['javas__sum'])

                    r.save()


            if skill=='php':
                r = cregister.objects.get(id=uid,php='True',sprint_id=sprid)
                ab = (r.vfphp)*(p.dev_working-r.planned-r.unplanned)
                r.abphp=ab
                r.spphp = r.abphp * 2
                sphp = cregister.objects.aggregate(Sum('spphp'))['spphp__sum']
                j = story.objects.filter(sprint_id=sprid, dev_php=r.name)
                if j.aggregate(Sum('phps'))['phps__sum'] == None:
                    list1.append(0)
                    r.dphp = r.spphp
                else:
                    list1.append(j.aggregate(Sum('phps'))['phps__sum'])
                    r.dphp = r.spphp - (j.aggregate(Sum('phps'))['phps__sum'])
                    r.save()


            if skill=='html':
                r = cregister.objects.get(id=uid,html='True',sprint_id=sprid)
                ab = (r.vfhtml)*(p.dev_working-r.planned-r.unplanned)
                r.abhtml=ab
                r.sphtml = r.abhtml * 2
                shtml = cregister.objects.aggregate(Sum('sphtml'))['sphtml__sum']
                j = story.objects.filter(sprint_id=sprid, dev_html=r.name)
                if j.aggregate(Sum('htmls'))['htmls__sum'] == None:
                    list1.append(0)
                    r.dhtml = r.sphtml
                else:
                    list1.append(j.aggregate(Sum('htmls'))['htmls__sum'])
                    r.dhtml = r.sphtml - (j.aggregate(Sum('htmls'))['htmls__sum'])
                    r.save()

            if skill=='qa':
                r = cregister.objects.get(id=uid,qa='True',sprint_id=sprid)
                ab = (r.vfqa)*(p.qa_working-r.planned-r.unplanned)
                r.abqa=ab
                r.spqa = r.abqa * 2
                sqa = cregister.objects.aggregate(Sum('spqa'))['spqa__sum']
                j = story.objects.filter(sprint_id=sprid, dev_qa=r.name)
                if j.aggregate(Sum('qas'))['qas__sum'] == None:
                    list1.append(0)
                    r.dqa = r.spqa
                else:
                    list1.append(j.aggregate(Sum('qas'))['qas__sum'])
                    r.dqa = r.spqa - (j.aggregate(Sum('qas'))['qas__sum'])
                    r.save()


        if 'leave1' in request.GET:
            pl = request.GET.get('leave1')
            uid = request.GET.get('leave2')
            skill = request.GET.get('leave3')
            r = cregister.objects.get(id=uid,sprint_id=sprid)
            r.planned = int(pl)
            p = product.objects.get(id=sprid)
            d2 = cregister.objects.filter(roles='dev',java='True',sprint_id=sprid)
            d3 = cregister.objects.filter(roles='dev',php='True',sprint_id=sprid)
            d4 = cregister.objects.filter(roles='dev',html='True',sprint_id=sprid)
            d5 = cregister.objects.filter(roles='dev',qa='True',sprint_id=sprid)
            r.save()

            if skill=='java':
                r = cregister.objects.get(id=uid,java='True',sprint_id=sprid)
                ab = (r.vfjava)*(p.dev_working-r.planned-r.unplanned)
                r.abjava=ab
                r.spjava = r.abjava * 2
                sjava = cregister.objects.aggregate(Sum('spjava'))['spjava__sum']
                j = story.objects.filter(sprint_id=sprid, dev_java=r.name)
                if j.aggregate(Sum('javas'))['javas__sum'] == None:
                    list1.append(0)
                    r.djava = r.spjava
                else:
                    list1.append(j.aggregate(Sum('javas'))['javas__sum'])
                    r.djava = r.spjava - (j.aggregate(Sum('javas'))['javas__sum'])
                    r.save()


            if skill=='php':
                r = cregister.objects.get(id=uid,php='True',sprint_id=sprid)
                ab = (r.vfphp)*(p.dev_working-r.planned-r.unplanned)
                r.abphp=ab
                r.spphp = r.abphp * 2
                sphp = cregister.objects.aggregate(Sum('spphp'))['spphp__sum']
                j = story.objects.filter(sprint_id=sprid, dev_php=r.name)
                if j.aggregate(Sum('phps'))['phps__sum'] == None:
                    list1.append(0)
                    r.dphp = r.spphp
                else:
                    list1.append(j.aggregate(Sum('phps'))['phps__sum'])
                    r.dphp = r.spphp - (j.aggregate(Sum('phps'))['phps__sum'])
                    r.save()


            if skill=='html':
                r = cregister.objects.get(id=uid,html='True',sprint_id=sprid)
                ab = (r.vfhtml)*(p.dev_working-r.planned-r.unplanned)
                r.abhtml=ab
                r.sphtml = r.abhtml * 2
                shtml = cregister.objects.aggregate(Sum('sphtml'))['sphtml__sum']
                j = story.objects.filter(sprint_id=sprid, dev_html=r.name)
                if j.aggregate(Sum('htmls'))['htmls__sum'] == None:
                    list1.append(0)
                    r.dhtml = r.sphtml
                else:
                    list1.append(j.aggregate(Sum('htmls'))['htmls__sum'])
                    r.dhtml = r.sphtml - (j.aggregate(Sum('htmls'))['htmls__sum'])
                    r.save()

            if skill=='qa':
                r = cregister.objects.get(id=uid,qa='True',sprint_id=sprid)
                ab = (r.vfqa)*(p.qa_working-r.planned-r.unplanned)
                r.abqa=ab
                r.spqa = r.abqa * 2
                sqa = cregister.objects.aggregate(Sum('spqa'))['spqa__sum']
                j = story.objects.filter(sprint_id=sprid, dev_qa=r.name)
                if j.aggregate(Sum('qas'))['qas__sum'] == None:
                    list1.append(0)
                    r.dqa = r.spqa
                else:
                    list1.append(j.aggregate(Sum('qas'))['qas__sum'])
                    r.dqa = r.spqa - (j.aggregate(Sum('qas'))['qas__sum'])
                    r.save()

    if request.method=='POST':
        if 'submit_sprint' in request.POST:
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
            return redirect('bandwidth')

    return(render(request,'bandwidth.html/',{'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'band':band,'d1':d1,'data':data,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'list1':list1,'list2':list2,'list3':list3,'list4':list4}))


@login_required
@user_passes_test(checkman,login_url='progress')
def allocation(request):
    id1 = request.session['id']
    pid2 = request.session['pid']
    data1 = product.objects.filter(pid=pid2)
    n = project.objects.all().exclude(id=0)
    nx = project.objects.get(id=pid2)
    nx1 = product.objects.get(id = id1).name
    d1 = cregister.objects.filter(roles='dev',sprint_id=id1)
    dashboard = story.objects.filter(sprint_id=id1)

    d2 = cregister.objects.filter(roles='dev',java='True',sprint_id=id1)
    d3 = cregister.objects.filter(roles='dev',php='True',sprint_id=id1)
    d4 = cregister.objects.filter(roles='dev',html='True',sprint_id=id1)
    d5 = cregister.objects.filter(roles='dev',qa='True',sprint_id=id1)

    sjava = cregister.objects.aggregate(Sum('spjava'))['spjava__sum']
    sphp = cregister.objects.aggregate(Sum('spphp'))['spphp__sum']
    shtml = cregister.objects.aggregate(Sum('sphtml'))['sphtml__sum']
    sqa = cregister.objects.aggregate(Sum('spqa'))['spqa__sum']

    list1=[]
    for i in d1:
        j = story.objects.filter(sprint_id=id1, dev_java=i.name)
        if j.aggregate(Sum('javas'))['javas__sum'] == None:
            list1.append(0)
        else:
            list1.append(j.aggregate(Sum('javas'))['javas__sum'])
    a=sum(list1)

    list2=[]
    for i in d1:
        j = story.objects.filter(sprint_id=id1, dev_php=i.name)
        if j.aggregate(Sum('phps'))['phps__sum'] == None:
            list2.append(0)
        else:
            list2.append(j.aggregate(Sum('phps'))['phps__sum'])
    b=sum(list2)

    list3=[]
    for i in d1:
        j = story.objects.filter(sprint_id=id1, dev_html=i.name)
        if j.aggregate(Sum('htmls'))['htmls__sum'] == None:
            list3.append(0)
        else:
            list3.append(j.aggregate(Sum('htmls'))['htmls__sum'])
    c=sum(list3)

    list4=[]
    for i in d1:
        j = story.objects.filter(sprint_id=id1, dev_qa=i.name)
        if j.aggregate(Sum('qas'))['qas__sum'] == None:
            list4.append(0)
        else:
            list4.append(j.aggregate(Sum('qas'))['qas__sum'])
    d=sum(list4)

    if request.method=='GET':
        if 'java_sel' in request.GET:
            java_dev = request.GET.get('java_sel')
            p1 = request.GET.get('points1')
            idy = request.GET.get('idx')
            if int(p1)>0:
                n = cregister.objects.get(name=java_dev,sprint_id=id1)
                p = story.objects.get(sprint_id=id1,id=idy)
                p.dev_java = java_dev
                p.javas = int(p1)
                p.save()
                list1=[]
                for i in d1:
                    j = story.objects.filter(sprint_id=id1, dev_java=i.name)
                    if j.aggregate(Sum('javas'))['javas__sum'] == None:
                        list1.append(0)
                    else:
                        list1.append(j.aggregate(Sum('javas'))['javas__sum'])
                        if p.ostatus in [None,'']:
                            p.ostatus='Live'
                        p.save()
                a=sum(list1)

        if 'php_sel' in request.GET:
            php_dev = request.GET.get('php_sel')
            p2 = request.GET.get('points2')
            idy = request.GET.get('idx')
            if int(p2)>0:
                n = cregister.objects.get(name=php_dev,sprint_id=id1)
                p = story.objects.get(sprint_id=id1,id=idy)
                p.dev_php = php_dev
                p.phps = int(p2)
                p.save()
                list2=[]
                for i in d1:
                    j = story.objects.filter(sprint_id=id1, dev_php=i.name)
                    if j.aggregate(Sum('phps'))['phps__sum'] == None:
                        list2.append(0)
                    else:
                        list2.append(j.aggregate(Sum('phps'))['phps__sum'])
                        if p.ostatus in [None,'']:
                            p.ostatus='Live'
                        p.save()
                b=sum(list2)

        if 'html_sel' in request.GET:
            html_dev = request.GET.get('html_sel')
            p3 = request.GET.get('points3')
            idy = request.GET.get('idx')
            if int(p3)>0:
                n = cregister.objects.get(name=html_dev,sprint_id=id1)
                p = story.objects.get(sprint_id=id1,id=idy)
                p.dev_html = html_dev
                p.htmls = int(p3)
                p.save()
                list3=[]
                for i in d1:
                    j = story.objects.filter(sprint_id=id1, dev_html=i.name)
                    if j.aggregate(Sum('htmls'))['htmls__sum'] == None:
                        list3.append(0)
                    else:
                        list3.append(j.aggregate(Sum('htmls'))['htmls__sum'])
                        if p.ostatus in [None,'']:
                            p.ostatus='Live'
                        p.save()
                c=sum(list3)

        if 'qa_sel' in request.GET:
            qa_dev = request.GET.get('qa_sel')
            p4 = request.GET.get('points4')
            idy = request.GET.get('idx')
            if int(p4)>0:
                n = cregister.objects.get(name=qa_dev,sprint_id=id1)
                p = story.objects.get(sprint_id=id1,id=idy)
                p.dev_qa = qa_dev
                p.qas = int(p4)
                p.save()
                list4=[]
                for i in d1:
                    j = story.objects.filter(sprint_id=id1, dev_qa=i.name)
                    if j.aggregate(Sum('qas'))['qas__sum'] == None:
                        list4.append(0)
                    else:
                        list4.append(j.aggregate(Sum('qas'))['qas__sum'])
                        if p.ostatus in [None,'']:
                            p.ostatus='Live'
                        p.save()
                d=sum(list4)
            return(redirect('allocation'))

    if request.method=='POST':
        if 'submit_sprint' in request.POST:
            select = request.POST.get('select_sprint')
            for i in data1:
                if select in i.name:
                    id=i.id
                    request.session['id'] = id
                    break
            return redirect('allocation')

        if 'select_project' in request.POST:
            name1 = request.POST.get('select_project')
            proid = project.objects.get(name=name1).id
            request.session['pid'] = proid
            return redirect('allocation')

    return render(request,'allocation.html/',{'data1':data1,'n':n,'nx':nx,'nx1':nx1,'dashboard':dashboard,'d1':d1,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'list1':list1,'list2':list2,'list3':list3,'list4':list4,'a':a,'b':b,'c':c,'d':d})

@login_required
def tasks(request):
    id1 = request.session['id']
    pid2 = request.session['pid']
    data1 = product.objects.filter(pid=pid2)
    n0 = project.objects.all().exclude(id=0)
    nx = project.objects.get(id=pid2)
    nx1 = product.objects.get(id = id1).name
    pro = product.objects.filter(pid=pid2)
    list1=[]
    k=0
    for i in pro:
        data1 = story.objects.filter(sprint_id=i.id)
        list1.append([])
        l=0
        for j in data1:
            list1[k].append([])
            list1[k][l].append(i.name)
            list1[k][l].append(j.story_name)
            list1[k][l].append(j.jira)
            if j.ostatus==None or j.ostatus=='':
                list1[k][l].append('Unassigned')
                list1[k][l].append('black')
            elif j.ostatus in ['Blocked','Blocked on API','Blocked on HTML','Blocked on Mock','Blocked on Spec']:
                list1[k][l].append(j.ostatus)
                list1[k][l].append('red')
            elif j.ostatus=='Live':
                list1[k][l].append(j.ostatus)
                list1[k][l].append('green')
            elif j.ostatus=='In Progress':
                list1[k][l].append(j.ostatus)
                list1[k][l].append('yellow')
            elif j.ostatus=='Next Sprint':
                list1[k][l].append(j.ostatus)
                list1[k][l].append('purple')
            elif j.ostatus in ['HTML Done','PHP Done','API Done','CR']:
                list1[k][l].append(j.ostatus)
                list1[k][l].append('white')
            elif j.ostatus=='QA':
                list1[k][l].append(j.ostatus)
                list1[k][l].append('blue')
            elif j.ostatus=='Pending Deployment':
                list1[k][l].append(j.ostatus)
                list1[k][l].append('pd')
            else:
                list1[k][l].append(j.ostatus)
                list1[k][l].append('other')
            list1[k][l].append(j.description)
            l+=1
        k+=1
    print(list1)

    if request.method=='POST':
        if 'select_project' in request.POST:
            name1 = request.POST.get('select_project')
            proid = project.objects.get(name=name1).id
            request.session['pid'] = proid
            return redirect('tasks')

    return(render(request,'tasks.html/',{'n0':n0,'nx':nx,'list1':list1}))

def home(request):
    return render(request,'home.html/',{})

def reg(request):
    total=story.objects.all().count()
    d1=register.objects.filter(roles='dev').count()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = registerform(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            x = user.username
            user.set_password(user.password)
            user.save()
            profile_form.instance.roles='dev'
            profile_form.instance.uname= x
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            return redirect('login/')
        else:
            print(user_form.errors , profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = registerform()
    return render(request , 'register.html' ,
                             {'user_form':user_form ,
                              'profile_form':profile_form ,
                              'registered':registered,'total':total,'d1':d1})


def log(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username = username , password = password)
    if request.method == 'POST':
        if user:
            if user.is_superuser:
                login(request,user)
                request.session['pid'] = 0
                return redirect('product')

            if user.is_active:
                login(request,user)
                request.session['pid'] = 0
                return redirect('product')
            else:
                return HttpResponse("Account not active!!")
        else:
            print("Someone tried to login and falied!")
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("Invalid credentials!")
    else:
        return render(request,'login.html/',{})
