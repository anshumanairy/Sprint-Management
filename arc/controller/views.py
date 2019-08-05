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
    if request.user.is_superuser:
        info = User.objects.get(username = request.user.username)
        check = 1
    else:
        check=0
        if cregister.objects.filter(uname = request.user.username,sprint_id = id1).exists()==True:
            info = cregister.objects.get(uname = request.user.username,sprint_id = id1)
        else:
            info = register.objects.get(uname = request.user.username)
    name = request.user.username
    if request.method=='POST':

        if 'update' in request.POST:
            if request.user.is_superuser:
                username = request.POST.get('uname')
                reg1 = User.objects.get(username=request.user.username)
                create = project.objects.filter(creator=request.user.username)
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
                reg2 = register.objects.get(uname=request.user.username)
                reg3 = cregister.objects.filter(uname=request.user.username)
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
    else:
        data1 = product.objects.filter(pid=pid2)
        sid = request.session['story_id']
        n0 = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = product.objects.get(id = id1).name
        name = request.user.username
        st = story.objects.filter(sprint_id=id1,id=sid)
        comm={}
        n=0
        for i in st:
            list2=list(map(str,i.comments.split('@change@')))
            comm[n]={}
            m=0
            for j in list2:
                if j!='':
                    comm[n][m]={}
                    list3=list(map(str,j.split('=')))
                    comm[n][m][list3[0]]=list3[1]
                    m+=1
            n+=1

        if request.method=='POST':
            if 'select_project' in request.POST:
                name1 = request.POST.get('select_project')
                proid = project.objects.get(name=name1).id
                request.session['pid'] = proid
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
            if 'comment_holder' in request.GET:
                comment=request.GET.get('comment_holder')
                id1 = request.GET.get('sid')
                stx = story.objects.get(id=id1)
                stx.comments = stx.comments + '@change@' + comment + '=' + request.user.username
                stx.save()
                return redirect('blog')

        return render(request,'blog.html/',{'name':name,'comm':comm,'st':st,'n0':n0,'nx':nx,'nx1':nx1,'data1':data1})


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
    if request.user.is_superuser or (cregister.objects.filter(uname=request.user.username,sprint_id=id1,roles='man').exists()==True):
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
                    list1[j][k].append(float(r.javas)-r.jactual)
                    if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_java).exists()==True:
                        z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_java).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r.javas)-r.jactual)
                elif r.dev_php==i.name:
                    list1[j][k].append(r.phps)
                    list1[j][k].append(r.ostatus)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r.pactual)
                    list1[j][k].append(float(r.phps)-r.pactual)
                    if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_php).exists()==True:
                        z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_php).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r.phps)-r.pactual)
                elif r.dev_html==i.name:
                    list1[j][k].append(r.htmls)
                    list1[j][k].append(r.ostatus)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r.hactual)
                    list1[j][k].append(float(r.htmls)-r.hactual)
                    if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_html).exists()==True:
                        z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_html).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r.htmls)-r.hactual)
                elif r.dev_qa==i.name:
                    list1[j][k].append(r.qas)
                    list1[j][k].append(r.ostatus)
                    list1[j][k].append(i.name)
                    list1[j][k].append(count)
                    list1[j][k].append(r.qactual)
                    list1[j][k].append(float(r.qas)-r.qactual)
                    if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_qa).exists()==True:
                        z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_qa).latest('id')
                        list1[j][k].append(z1.left)
                    else:
                        list1[j][k].append(float(r.qas)-r.qactual)

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
                    st = story.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                    cx=0
                    for ix in st:
                        if ix.dev_java==n2:
                            if float(left1)==(float(ix.javas)-ix.jactual):
                                left1 = (float(ix.javas)-(ix.jactual+ frac1))
                            ix.jactual = ix.jactual + frac1
                            ix.jleft = left1
                            cx=float(ix.javas)-float(left1)
                        elif ix.dev_php==n2:
                            if float(left1)==(float(ix.phps)-ix.pactual):
                                left1 = (float(ix.phps)-(ix.pactual+ frac1))
                            ix.pactual = ix.pactual + frac1
                            ix.pleft = left1
                            cx=float(ix.phps)-float(left1)
                        elif ix.dev_html==n2:
                            if float(left1)==(float(ix.htmls)-ix.hactual):
                                left1 = (float(ix.htmls)-(ix.hactual+ frac1))
                            ix.hactual = ix.hactual + frac1
                            ix.hleft = left1
                            cx=float(ix.htmls)-float(left1)
                        else:
                            if float(left1)==(float(ix.qas)-ix.qactual):
                                left1 = (float(ix.qas)-(ix.qactual+ frac1))
                            ix.qactual = ix.qactual + frac1
                            ix.qleft = left1
                            cx=float(ix.qas)-float(left1)
                        ix.save()
                        z = prg(s_id=id1,jd=j,sdate=stdate,status=prog,dname=n2,actual=frac1,left=left1,cl=cx)
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
                else:
                    messages.info(request, 'Please select a Valid Date!')

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
        name=request.user.username
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
                list1[j][k].append(r.jactual)
                if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_java).exists()==True:
                    z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_java).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.javas)-r.jactual)
            elif r.dev_php==name1:
                list1[j][k].append(r.phps)
                list1[j][k].append(r.ostatus)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.pactual)
                if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_php).exists()==True:
                    z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_php).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.phps)-r.pactual)
            elif r.dev_html==name1:
                list1[j][k].append(r.htmls)
                list1[j][k].append(r.ostatus)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.hactual)
                if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_html).exists()==True:
                    z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_html).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.htmls)-r.hactual)
            elif r.dev_qa==name1:
                list1[j][k].append(r.qas)
                list1[j][k].append(r.ostatus)
                list1[j][k].append(name1)
                list1[j][k].append(count)
                list1[j][k].append(r.qactual)
                if prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_qa).exists()==True:
                    z1 = prg.objects.filter(s_id=id1,jd=r.jira,dname=r.dev_qa).latest('id')
                    list1[j][k].append(z1.left)
                else:
                    list1[j][k].append(float(r.qas)-r.qactual)
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
                    st = story.objects.filter(sprint_id=id1,dev_java=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_php=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_html=n2,jira=j) | story.objects.filter(sprint_id=id1,dev_qa=n2,jira=j)
                    cx=0
                    for ix in st:
                        if ix.dev_java==n2:
                            if float(left1)==(float(ix.javas)-ix.jactual):
                                left1 = (float(ix.javas)-(ix.jactual+ frac1))
                            ix.jactual = ix.jactual + frac1
                            ix.jleft = left1
                            cx=float(ix.javas)-float(left1)
                        elif ix.dev_php==n2:
                            if float(left1)==(float(ix.phps)-ix.pactual):
                                left1 = (float(ix.phps)-(ix.pactual+ frac1))
                            ix.pactual = ix.pactual + frac1
                            ix.pleft = left1
                            cx=float(ix.phps)-float(left1)
                        elif ix.dev_html==n2:
                            if float(left1)==(float(ix.htmls)-ix.hactual):
                                left1 = (float(ix.htmls)-(ix.hactual+ frac1))
                            ix.hactual = ix.hactual + frac1
                            ix.hleft = left1
                            cx=float(ix.htmls)-float(left1)
                        else:
                            if float(left1)==(float(ix.qas)-ix.qactual):
                                left1 = (float(ix.qas)-(ix.qactual+ frac1))
                            ix.qactual = ix.qactual + frac1
                            ix.qleft = left1
                            cx=float(ix.qas)-float(left1)
                        ix.save()
                        z = prg(s_id=id1,jd=j,sdate=stdate,status=prog,dname=n2,actual=frac1,left=left1,cl=cx)
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
                return redirect('qaprg')

    return(render(request,'qaprg.html/',{'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'data':data,'list1':list1,'p':p,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'d1':jd1,'d2':jd2,'d3':jd3}))

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
    cal=0
    if product.objects.filter(id=id,pid=pid2).exists()==True:
        p1 = product.objects.get(id=id,pid=pid2)
    else:
        p1 = product.objects.get(id=0,pid=0)
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
    s1 = story.objects.filter(sprint_id=id)
    sum1=0
    sum2=0
    sumx=0
    for i1 in s1:
        sum1 += i1.jleft + i1.pleft + i1.hleft + i1.qleft
        sum2 += i1.javas + i1.phps + i1.htmls + i1.qas
        if i1.ostatus in['QA']:
            list7[1]+=1
        if i1.ostatus in['In Progress','HTML Done','PHP Done','API Done','Blocked','Blocked on API','Blocked on HTML','Blocked on Mock','Blocked on Spec','CR']:
            list7[2]+=1
        if i1.ostatus in['Live','Pending Deployment','Complete']:
            list7[0]+=1
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
            p2 = prg.objects.filter(s_id=id,sdate=dt.strftime("%Y-%m-%d"))
            s2=0
            s3=0
            s4=0
            s6=0
            for i2 in p2:
                s5 = story.objects.get(sprint_id=id,jira=i2.jd)
                if s5.dev_java==i2.dname:
                    s4+=s5.javas
                elif s5.dev_php==i2.dname:
                    s4+=s5.phps
                elif s5.dev_html==i2.dname:
                    s4+=s5.htmls
                elif s5.dev_qa==i2.dname:
                    s4+=s5.qas

                s2+=i2.actual
                s3+=i2.left
                s6+=i2.cl

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
    s22 = cregister.objects.filter(sprint_id=id).exclude(sprint_id=0)
    hx2 = product.objects.get(id=id).name
    if userxx == user3:
        hx1 = user3
        if cregister.objects.filter(sprint_id=id,name=user3).exists()==True:
            s2 = cregister.objects.get(sprint_id=id,name=user3)
        else:
            s2 = cregister.objects.get(sprint_id=0,name='')

        s3 = story.objects.filter(sprint_id=id,dev_java=user3) or story.objects.filter(sprint_id=id,dev_php=user3) or story.objects.filter(sprint_id=id,dev_html=user3) or story.objects.filter(sprint_id=id,dev_qa=user3)
        list8=[]
        sp=0
        sc=0
        ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
        for i4 in s3:
            if i4.dev_java==user3:
                sp+=i4.javas
                sc+=i4.jactual
            elif i4.dev_php==user3:
                sp+=i4.phps
                sc+=i4.pactual
            elif i4.dev_html==user3:
                sp+=i4.htmls
                sc+=i4.hactual
            elif i4.dev_qa==user3:
                sp+=i4.qas
                sc+=i4.qactual

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
            s3 = story.objects.filter(sprint_id=id,dev_java=s2.name) or story.objects.filter(sprint_id=id,dev_php=s2.name) or story.objects.filter(sprint_id=id,dev_html=s2.name) or story.objects.filter(sprint_id=id,dev_qa=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.javas
                    sc+=i4.jactual
                elif i4.dev_php==s2.name:
                    sp+=i4.phps
                    sc+=i4.pactual
                elif i4.dev_html==s2.name:
                    sp+=i4.htmls
                    sc+=i4.hactual
                elif i4.dev_qa==s2.name:
                    sp+=i4.qas
                    sc+=i4.qactual
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
        s22 = cregister.objects.filter(sprint_id=id,java=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story.objects.filter(sprint_id=id,dev_java=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.javas
                    sc+=i4.jactual
                elif i4.dev_php==s2.name:
                    sp+=i4.phps
                    sc+=i4.pactual
                elif i4.dev_html==s2.name:
                    sp+=i4.htmls
                    sc+=i4.hactual
                elif i4.dev_qa==s2.name:
                    sp+=i4.qas
                    sc+=i4.qactual
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
        s22 = cregister.objects.filter(sprint_id=id,php=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story.objects.filter(sprint_id=id,dev_php=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.javas
                    sc+=i4.jactual
                elif i4.dev_php==s2.name:
                    sp+=i4.phps
                    sc+=i4.pactual
                elif i4.dev_html==s2.name:
                    sp+=i4.htmls
                    sc+=i4.hactual
                elif i4.dev_qa==s2.name:
                    sp+=i4.qas
                    sc+=i4.qactual
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
        s22 = cregister.objects.filter(sprint_id=id,html=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story.objects.filter(sprint_id=id,dev_html=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.javas
                    sc+=i4.jactual
                elif i4.dev_php==s2.name:
                    sp+=i4.phps
                    sc+=i4.pactual
                elif i4.dev_html==s2.name:
                    sp+=i4.htmls
                    sc+=i4.hactual
                elif i4.dev_qa==s2.name:
                    sp+=i4.qas
                    sc+=i4.qactual
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
        s22 = cregister.objects.filter(sprint_id=id,qa=True).exclude(sprint_id=0)
        for s2 in s22:
            s3 = story.objects.filter(sprint_id=id,dev_qa=s2.name)
            sp=0
            sc=0
            ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
            for i4 in s3:
                if i4.dev_java==s2.name:
                    sp+=i4.javas
                    sc+=i4.jactual
                elif i4.dev_php==s2.name:
                    sp+=i4.phps
                    sc+=i4.pactual
                elif i4.dev_html==s2.name:
                    sp+=i4.htmls
                    sc+=i4.hactual
                elif i4.dev_qa==s2.name:
                    sp+=i4.qas
                    sc+=i4.qactual
            list9.append(ab)
            list9.append(sp)
            list9.append(sc)
            list10.append(s2.name)
        jd8 = json.dumps(list9)
        val=json.dumps('QA Dev')
        nval=json.dumps(list10)

    data = product.objects.filter(pid=pid2)
    n = project.objects.all().exclude(id=0)
    nx = project.objects.get(id=pid2)
    form = productform(request.POST or None)
    list11=[]
    z1 = User.objects.all()
    for i11 in z1:
        if i11.is_superuser:
            list11.append(i11.username)

    z2 = register.objects.all()
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
                p1 = product.objects.get(id=id,pid=pid2)
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
            if request.user.is_superuser and request.user.username == user1:
                for i in n:
                    if name1==i.name:
                        a+=1
                        messages.info(request, 'Project Name already taken. Please choose another one!')
                        return redirect('product')
                if a==0:
                    z = project(name = name1,devs=c,mans=d,creator=user1)
                    z.save()
            else:
                messages.info(request, 'You are not Authorized!')
                return redirect('product')

            return(redirect('product'))

        if 'select_project' in request.POST:
            name1 = request.POST.get('select_project')
            proid = project.objects.get(name=name1).id
            request.session['pid'] = proid
            return(redirect('product'))

        if 'select_user' in request.POST:
            user1 = request.POST.get('select_user')
            if user1 not in ['All Developers','Java Dev','PHP Dev','HTML Dev','QA Dev']:
                request.session['user2'] = user1
                request.session['userx'] = user1
                s2 = cregister.objects.get(sprint_id=id,name=user1)
                s3 = story.objects.filter(sprint_id=id,dev_java=user1) or story.objects.filter(sprint_id=id,dev_php=user1) or story.objects.filter(sprint_id=id,dev_html=user1) or story.objects.filter(sprint_id=id,dev_qa=user1)
                list8=[]
                sp=0
                sc=0
                ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                for i4 in s3:
                    if i4.dev_java==user1:
                        sp+=i4.javas
                        sc+=i4.jactual
                    elif i4.dev_php==user1:
                        sp+=i4.phps
                        sc+=i4.pactual
                    elif i4.dev_html==user1:
                        sp+=i4.htmls
                        sc+=i4.hactual
                    elif i4.dev_qa==user1:
                        sp+=i4.qas
                        sc+=i4.qactual
                list8.append(ab)
                list8.append(sp)
                list8.append(sc)
                jd8 = json.dumps(list8)
                nval=json.dumps('')
                val=json.dumps('Single')

            if user1 == "All Developers":
                request.session['userx'] = 'Users'
                s22 = cregister.objects.filter(sprint_id=id).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story.objects.filter(sprint_id=id,dev_java=s2.name) or story.objects.filter(sprint_id=id,dev_php=s2.name) or story.objects.filter(sprint_id=id,dev_html=s2.name) or story.objects.filter(sprint_id=id,dev_qa=s2.name)
                    sp=0
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.javas
                            sc+=i4.jactual
                        elif i4.dev_php==s2.name:
                            sp+=i4.phps
                            sc+=i4.pactual
                        elif i4.dev_html==s2.name:
                            sp+=i4.htmls
                            sc+=i4.hactual
                        elif i4.dev_qa==s2.name:
                            sp+=i4.qas
                            sc+=i4.qactual
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('All Developers')
                    nval=json.dumps(list10)

            if user1 == "Java Dev":
                request.session['userx'] = 'Java'
                s22 = cregister.objects.filter(sprint_id=id,java=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story.objects.filter(sprint_id=id,dev_java=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.javas
                            sc+=i4.jactual
                        elif i4.dev_php==s2.name:
                            sp+=i4.phps
                            sc+=i4.pactual
                        elif i4.dev_html==s2.name:
                            sp+=i4.htmls
                            sc+=i4.hactual
                        elif i4.dev_qa==s2.name:
                            sp+=i4.qas
                            sc+=i4.qactual
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('Java Dev')
                    nval=json.dumps(list10)

            if user1 == "PHP Dev":
                request.session['userx'] = 'PHP'
                s22 = cregister.objects.filter(sprint_id=id,php=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story.objects.filter(sprint_id=id,dev_php=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.javas
                            sc+=i4.jactual
                        elif i4.dev_php==s2.name:
                            sp+=i4.phps
                            sc+=i4.pactual
                        elif i4.dev_html==s2.name:
                            sp+=i4.htmls
                            sc+=i4.hactual
                        elif i4.dev_qa==s2.name:
                            sp+=i4.qas
                            sc+=i4.qactual
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('PHP Dev')
                    nval=json.dumps(list10)

            if user1 == "HTML Dev":
                request.session['userx'] = 'HTML'
                s22 = cregister.objects.filter(sprint_id=id,html=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story.objects.filter(sprint_id=id,dev_html=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.javas
                            sc+=i4.jactual
                        elif i4.dev_php==s2.name:
                            sp+=i4.phps
                            sc+=i4.pactual
                        elif i4.dev_html==s2.name:
                            sp+=i4.htmls
                            sc+=i4.hactual
                        elif i4.dev_qa==s2.name:
                            sp+=i4.qas
                            sc+=i4.qactual
                    list9.append(ab)
                    list9.append(sp)
                    list9.append(sc)
                    list10.append(s2.name)
                    jd8 = json.dumps(list9)
                    val=json.dumps('HTML Dev')
                    nval=json.dumps(list10)

            if user1 == "QA Dev":
                request.session['userx'] = 'QA'
                s22 = cregister.objects.filter(sprint_id=id,qa=True).exclude(sprint_id=0)
                list9=[]
                list10=[]
                for s2 in s22:
                    s3 = story.objects.filter(sprint_id=id,dev_qa=s2.name)
                    sc=0
                    ab = s2.spjava + s2.spphp + s2.sphtml +s2.spqa
                    for i4 in s3:
                        if i4.dev_java==s2.name:
                            sp+=i4.javas
                            sc+=i4.jactual
                        elif i4.dev_php==s2.name:
                            sp+=i4.phps
                            sc+=i4.pactual
                        elif i4.dev_html==s2.name:
                            sp+=i4.htmls
                            sc+=i4.hactual
                        elif i4.dev_qa==s2.name:
                            sp+=i4.qas
                            sc+=i4.qactual
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
            if request.user.is_superuser or (cregister.objects.filter(uname=request.user.username,sprint_id=id1,roles='man').exists()==True) or (register.objects.filter(uname=request.user.username,roles='man').exists()==True):
                if form.is_valid():
                    form = productform(request.POST)
                    form.instance.pid = pid2
                    form.instance.sprint_start_date=start
                    form.instance.sprint_dev_end_date=dev
                    form.instance.sprint_qa_end_date=qa
                    form.save()
                    x = form.instance.id
                    x1 = register.objects.all()
                    obj = project.objects.get(id=pid2)
                    selected_users = list(map(str,(obj.devs).split('@end@')))
                    selected_mans = list(map(str,(obj.mans).split('@end@')))
                    for i1 in x1:
                        if i1.uname in selected_mans:
                            x2 = cregister(sprint_id=x,uname=i1.uname,name=i1.name,roles='man',java=i1.java,html=i1.html,php=i1.php,qa=i1.php)
                            # x2.save()
                        else:
                            if i1.uname in selected_users:
                                x2 = cregister(sprint_id=x,uname=i1.uname,name=i1.name,roles=i1.roles,java=i1.java,html=i1.html,php=i1.php,qa=i1.php)
                                # x2.save()
                    return redirect('product')
                else:
                    messages.info(request, 'Data Not Stored!')
                    return redirect('product')
            else:
                messages.info(request, 'You are not Authorized!')
                return redirect('product')
        else:
            form = productform()

    return(render(request,'product.html/',context={'name':name,'z2':z2,'nval':nval,'val':val,'hx2':hx2,'hx1':hx1,'jd8':jd8,'s22':s22,'jd7':jd7,'jd6':jd6,'jd5':jd5,'jd1':jd1,'form':form,'data':data,'n':n,'nx':nx,'list11':list11}))

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
    if request.user.is_superuser or (cregister.objects.filter(uname=request.user.username,sprint_id=id,roles='man').exists()==True):
        data1 = product.objects.filter(pid=pid2)
        n = project.objects.all().exclude(id=0)
        nx = project.objects.get(id=pid2)
        nx1 = product.objects.get(id = id).name
        data = story.objects.filter(sprint_id=id)

        #progress part
        datax = cregister.objects.filter(roles='dev',sprint_id=id)
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
            if i1.dev_java not in ['',None]:
                list2x[i1.jira]={}
                list3x[i1.jira]={}
                if prg.objects.filter(s_id=id,dname=i1.dev_java,jd=i1.jira).exists()==True:
                    st1 = prg.objects.filter(s_id=id,dname=i1.dev_java,jd=i1.jira)
                    list2x[i1.jira][ny]={}
                    list3x[i1.jira][ny]={}
                    xy=0
                    for i2 in st1:
                        list2x[i1.jira][ny][str(xy)]=str(i2.sdate)
                        list3x[i1.jira][ny][str(xy)]=i2.status
                        xy+=1

            py+=1
            if i1.dev_php not in ['',None]:
                list4x[i1.jira]={}
                list5x[i1.jira]={}
                if prg.objects.filter(s_id=id,dname=i1.dev_php,jd=i1.jira).exists()==True:
                    st1 = prg.objects.filter(s_id=id,dname=i1.dev_php,jd=i1.jira)
                    list4x[i1.jira][py]={}
                    list5x[i1.jira][py]={}
                    xy=0
                    for i2 in st1:
                        list4x[i1.jira][py][str(xy)]=str(i2.sdate)
                        list5x[i1.jira][py][str(xy)]=i2.status
                        xy+=1

            hy+=1
            if i1.dev_html not in ['',None]:
                list6x[i1.jira]={}
                list7x[i1.jira]={}
                if prg.objects.filter(s_id=id,dname=i1.dev_html,jd=i1.jira).exists()==True:
                    st1 = prg.objects.filter(s_id=id,dname=i1.dev_html,jd=i1.jira)
                    list6x[i1.jira][hy]={}
                    list7x[i1.jira][hy]={}
                    xy=0
                    for i2 in st1:
                        list6x[i1.jira][hy][str(xy)]=str(i2.sdate)
                        list7x[i1.jira][hy][str(xy)]=i2.status
                        xy+=1

            qy+=1
            if i1.dev_qa not in ['',None]:
                list8x[i1.jira]={}
                list9x[i1.jira]={}
                if prg.objects.filter(s_id=id,dname=i1.dev_qa,jd=i1.jira).exists()==True:
                    st1 = prg.objects.filter(s_id=id,dname=i1.dev_qa,jd=i1.jira)
                    list8x[i1.jira][qy]={}
                    list9x[i1.jira][qy]={}
                    xy=0
                    for i2 in st1:
                        list8x[i1.jira][qy][str(xy)]=str(i2.sdate)
                        list9x[i1.jira][qy][str(xy)]=i2.status
                        xy+=1

        jd1x=json.dumps(list2x)
        jd2x=json.dumps(list3x)
        jd3x=json.dumps(list4x)
        jd4x=json.dumps(list5x)
        jd5x=json.dumps(list6x)
        jd6x=json.dumps(list7x)
        jd7x=json.dumps(list8x)
        jd8x=json.dumps(list9x)

        px = product.objects.get(id=id)
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
        d1 = cregister.objects.filter(roles='dev',sprint_id=id)
        d2 = cregister.objects.filter(roles='dev',java='True',sprint_id=id)
        d3 = cregister.objects.filter(roles='dev',php='True',sprint_id=id)
        d4 = cregister.objects.filter(roles='dev',html='True',sprint_id=id)
        d5 = cregister.objects.filter(roles='dev',qa='True',sprint_id=id)
        sjava = cregister.objects.aggregate(Sum('spjava'))['spjava__sum']
        sphp = cregister.objects.aggregate(Sum('spphp'))['spphp__sum']
        shtml = cregister.objects.aggregate(Sum('sphtml'))['sphtml__sum']
        sqa = cregister.objects.aggregate(Sum('spqa'))['spqa__sum']
        list11=[]
        for i in d1:
            j = story.objects.filter(sprint_id=id, dev_java=i.name)
            if j.aggregate(Sum('javas'))['javas__sum'] == None:
                list11.append(0)
            else:
                list11.append(j.aggregate(Sum('javas'))['javas__sum'])
        a=sum(list11)

        list21=[]
        for i in d1:
            j = story.objects.filter(sprint_id=id, dev_php=i.name)
            if j.aggregate(Sum('phps'))['phps__sum'] == None:
                list21.append(0)
            else:
                list21.append(j.aggregate(Sum('phps'))['phps__sum'])
        b=sum(list21)

        list31=[]
        for i in d1:
            j = story.objects.filter(sprint_id=id, dev_html=i.name)
            if j.aggregate(Sum('htmls'))['htmls__sum'] == None:
                list31.append(0)
            else:
                list31.append(j.aggregate(Sum('htmls'))['htmls__sum'])
        c=sum(list31)

        list41=[]
        for i in d1:
            j = story.objects.filter(sprint_id=id, dev_qa=i.name)
            if j.aggregate(Sum('qas'))['qas__sum'] == None:
                list41.append(0)
            else:
                list41.append(j.aggregate(Sum('qas'))['qas__sum'])
        d=sum(list41)

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
        name=request.user.username
        if request.method=='GET':
            if 'red' in request.GET:
                idx = request.GET.get('red')
                request.session['story_id'] = idx
                return(redirect('story'))

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

            if 'assign_data' in request.GET:
                java_dev = request.GET.get('java_sel')
                p1 = request.GET.get('points1')
                idy = request.GET.get('idx')
                if int(p1)>0:
                    # n = cregister.objects.get(name=java_dev,sprint_id=id1)
                    p = story.objects.get(sprint_id=id,id=idy)
                    p.dev_java = java_dev
                    p.javas = int(p1)
                    p.jleft = int(p1)
                    p.save()
                    list1=[]
                    for i in d1:
                        j = story.objects.filter(sprint_id=id, dev_java=i.name)
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
                    # n = cregister.objects.get(name=php_dev,sprint_id=id1)
                    p = story.objects.get(sprint_id=id,id=idy)
                    p.dev_php = php_dev
                    p.phps = int(p2)
                    p.pleft = int(p2)
                    p.save()
                    list2=[]
                    for i in d1:
                        j = story.objects.filter(sprint_id=id, dev_php=i.name)
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
                    # n = cregister.objects.get(name=html_dev,sprint_id=id1)
                    p = story.objects.get(sprint_id=id,id=idy)
                    p.dev_html = html_dev
                    p.htmls = int(p3)
                    p.hleft = int(p3)
                    p.save()
                    list3=[]
                    for i in d1:
                        j = story.objects.filter(sprint_id=id, dev_html=i.name)
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
                    # n = cregister.objects.get(name=qa_dev,sprint_id=id1)
                    p = story.objects.get(sprint_id=id,id=idy)
                    p.dev_qa = qa_dev
                    p.qas = int(p4)
                    p.qleft = int(p4)
                    p.save()
                    list4=[]
                    for i in d1:
                        j = story.objects.filter(sprint_id=id, dev_qa=i.name)
                        if j.aggregate(Sum('qas'))['qas__sum'] == None:
                            list4.append(0)
                        else:
                            list4.append(j.aggregate(Sum('qas'))['qas__sum'])
                            if p.ostatus in [None,'']:
                                p.ostatus='Live'
                            p.save()
                    d=sum(list4)
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
                                if fields[10] in ['Complete','Live','In Progress','HTML Done','PHP Done','API Done','QA','Pending Deployment','Blocked','Blocked on API','Blocked on HTML','Blocked on Mock','Blocked on Spec','Not Needed','Next Sprint','Duplicate','CR','',' ']:
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
                            messages.info(request, 'Jira ID already exists. Please choose another one!')
                            return redirect('view_story')
                    form.save()
                    return redirect('view_story')
                else:
                    messages.info(request, 'Data Not Stored!')
                    return redirect('view_story')
            else:
                form = storyform()

        return render(request,'view_story.html',{'jd8x':jd8x,'jd7x':jd7x,'jd6x':jd6x,'jd5x':jd5x,'jd4x':jd4x,'jd3x':jd3x,'aa':aa,'bb':bb,'cc':cc,'dd':dd,'ee':ee,'ff':ff,'jd1x':jd1x,'jd2x':jd2x,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'dashboard':dashboard,'list11':list11,'list21':list21,'list31':list31,'list41':list41,'a':a,'b':b,'c':c,'d':d,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'d1':d1,'form':form,'data':data,'jd1':jd1,'jd2':jd2,'jd3':jd3,'jd4':jd4,'n':n,'nx':nx,'data1':data1,'nx1':nx1,'name':name})
    else:
        return(redirect('qaprg'))

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
    if request.user.is_superuser or (cregister.objects.filter(uname=request.user.username,sprint_id=sprid,roles='man').exists()==True):
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
        name=request.user.username
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
                return redirect('bandwidth')

        return(render(request,'bandwidth.html/',{'name':name,'data1':data1,'n0':n0,'nx':nx,'nx1':nx1,'band':band,'d1':d1,'data':data,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'sjava':sjava,'sphp':sphp,'shtml':shtml,'sqa':sqa,'list1':list1,'list2':list2,'list3':list3,'list4':list4}))
    else:
        return(redirect(qaprg))

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
    data1 = product.objects.filter(pid=pid2)
    data3 = product.objects.filter(pid=pid2).exclude(id=id1)
    list1x=[]
    list2x=[]
    list3x=[]

    if request.user.is_superuser or (cregister.objects.filter(uname=request.user.username,sprint_id=id1,roles='man').exists()==True):
        pass
    else:
        u1 = register.objects.get(uname=request.user.username)
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
        k3 = product.objects.filter(pid=k2.id).exclude(id=id1)
        m=0
        for k4 in k3:
            listse[n].append([])
            if k4.sprint_dev_end_date>=k4.sprint_qa_end_date:
                if k4.sprint_dev_end_date>=datetime.date.today():
                    listse[n][m].append(k4.name)
                    listse[n][m].append(k4.id)
                    m+=1
            else:
                if k4.sprint_qa_end_date>=datetime.date.today():
                    listse[n][m].append(k4.name)
                    listse[n][m].append(k4.id)
                    m+=1
        n+=1

    n0 = project.objects.all().exclude(id=0)
    nx = project.objects.get(id=pid2)
    nx1 = product.objects.get(id = id1).name
    pro = product.objects.filter(pid=pid2)


    k=0
    repo=[]
    c1 = cregister.objects.filter(sprint_id=id1,roles='dev')
    sum3=0
    for i3 in c1:
        sum3+=i3.abjava + i3.abphp + i3.abhtml + i3.abqa
    repo.append(sum3)
    sum1=0
    sum2=0
    nextspr=[]
    c2 = story.objects.filter(sprint_id=id1)
    for i4 in c2:
        sum1+= i4.javas + i4.phps + i4.htmls + i4.qas
        sum2+=i4.jactual + i4.pactual + i4.hactual + i4.qactual
        if i4.ostatus not in ['Pending Deployment','Complete','Live']:
            nextspr.append(i4.id)

    repo.append(sum1)
    repo.append(sum1-sum2)
    repo.append(sum2)

    list1=[]
    name = request.user.username
    xx=0
    for i in pro:
        data2 = story.objects.filter(sprint_id=i.id)
        list1.append([])
        l=0
        for j in data2:
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
            elif j.ostatus in ['Pending Deployment','Complete']:
                list1[k][l].append(j.ostatus)
                list1[k][l].append('pd')
            else:
                list1[k][l].append(j.ostatus)
                list1[k][l].append('other')
            list1[k][l].append(j.description)
            list1[k][l].append(j.javas + j.phps + j.htmls + j.qas)
            list1[k][l].append((j.javas + j.phps + j.htmls + j.qas)-(j.jactual + j.pactual + j.hactual + j.qactual))
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
            if request.user.is_superuser or (cregister.objects.filter(uname=request.user.username,sprint_id=id1,roles='man').exists()==True):
                messages.info(request, 'Sorry authority only with Developer. Please allocate points from the story board!')
            else:
                if skill in ['java','php','html','qa']:
                    pro = product.objects.get(name=sprname,pid=pid2).id
                    st = story.objects.get(sprint_id=pro,jira=jd)
                    listz=[]
                    u1 = register.objects.get(uname=request.user.username)
                    if u1.java==True:
                        listz.append('java')
                    if u1.php==True:
                        listz.append('php')
                    if u1.html==True:
                        listz.append('html')
                    if u1.qa==True:
                        listz.append('qa')
                    if skill in listz:
                        st.ostatus='In Progress'
                        if skill=='java':
                            st.dev_java=u1.name
                            st.javas=int(pt)
                        elif skill=='php':
                            st.dev_php=u1.name
                            st.phps=int(pt)
                        elif skill=='html':
                            st.dev_html=u1.name
                            st.htmls=int(pt)
                        elif skill=='qa':
                            st.dev_qa=u1.name
                            st.qas=int(pt)
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
            return redirect('tasks')

        if 'select_sprint' in request.POST:
            select = request.POST.get('select_sprint')
            for i in data1:
                if select in i.name:
                    id=i.id
                    request.session['id'] = id
                    break
            return redirect('tasks')

        if 'move_story' in request.POST:
            if request.user.is_superuser:
                ss = request.POST.get('select_spr')
                st1 = story.objects.filter(sprint_id=id1)
                for i1 in st1:
                    if i1.ostatus not in ['Pending Deployment','Complete']:
                        x1 = story(sprint_id=ss,story_name=i1.story_name,description=i1.description,jira=i1.jira)
                        x1.save()
                        i1.delete()
                        i1.save()
                messages.info(request, 'Success!')
                return redirect('tasks')
            else:
                messages.info(request, 'You are not Authorized!')
                return redirect('tasks')

    return(render(request,'tasks.html/',{'name':name,'jd1x':jd1x,'jd2x':jd2x,'jd3x':jd3x,'listse':listse,'repo':repo,'data1':data1,'nx1':nx1,'n0':n0,'nx':nx,'list1':list1}))

def home(request):
    return render(request,'home.html/',{})

def reg(request):
    total=story.objects.all().count()
    d1=User.objects.all().count()
    name=''
    email=''
    emp=0
    registered = False
    try:
        if request.method =='GET':
            auth_code = request.GET.get('auth_code', '')
            encrypt_auth = encryptx(auth_code)

            # part2 to obtain token
            payload = {
                    'grantType':'authorization_code',
                    'code':encrypt_auth,
                    'clientId':'SprintManagement'
                    }

            headers = {
                    'Authorization':'Basic JaA+KUfutRpIkHY54Scvn9B3XAbg3sq3enrRREIv344=',
                    'X-Quikr-Client':'Platform',
                    'Content-Type':'application/json'
                    }

            response = requests.request("POST",'http://192.168.124.123:13000/identity/v1/token', data=json.dumps(payload), headers=headers)
            resp = response.text
            list1=list(map(str,resp.split('"')))
            idtoken = list1[5]
            access_token = auth_code
            list2=list(map(str,idtoken.split('.')))
            dec = decryptx(list1[5])

            emp = dec['empId']
            print(emp)
            email = dec['email']
            name = dec['name']

            if User.objects.filter(email=email).exists() == True:
                regx = User.objects.get(email=email)
                user = authenticate(username = regx.username, password='Zehel9999')
                login(request,user)
                request.session['pid'] = 0
                request.session['user2'] = ''
                request.session['id'] = 0
                request.session['userx'] = 'Users'
                return redirect('product')
    except:
        pass


    # email = 'anshuman.airy@quikr.com'
    #
    # if User.objects.filter(email=email).exists() == True:
    #     regx = User.objects.get(email=email)
    #     user = authenticate(username = regx.username, password='Zehel9999')
    #     login(request,user)
    #     request.session['pid'] = 0
    #     request.session['user2'] = ''
    #     request.session['id'] = 0
    #     request.session['userx'] = 'Users'
    #     return redirect('product')

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = registerform(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            x = user.username
            profile_form.instance.uname= x
            profile = profile_form.save(commit=False)
            if ((user.email==email) and (profile.empid==emp) and (profile.name==name)):
                user.set_password('Zehel9999')
                user.save()
                profile.user = user
                profile.save()
                registered = True
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
