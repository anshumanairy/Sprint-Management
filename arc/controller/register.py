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

def reg(request):
    total=story.objects.all().count()
    d1=User.objects.all().count()
    name=''
    email=''
    emp=0
    registered = False

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

    try:
        if request.method =='GET':
            
            #part1 to obtain authorization code
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

            emp = int(dec['empId'])
            email = dec['email']
            name = dec['name']
            request.session['emp'] = emp
            request.session['email'] = email
            request.session['name'] = name

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

def log(request):
    return redirect("http://192.168.124.123:13000/identity/v1/auth?auth=Basic%20JaA%2BKUfutRpIkHY54Scvn9B3XAbg3sq3enrRREIv344%3D&clientId=SprintManagement&redirectUri=http%3A%2F%2F127.0.0.1%3A8000%2F&responseType=code&scope=openid")


@login_required(login_url='/')
def user_logout(request):
    logout(request)
    # request.session.flush()
    response = redirect('/')
    response.delete_cookie('sessionid', domain="127.0.0.1",path='/')
    response.delete_cookie('csrftoken', domain="127.0.0.1",path='/')
    return response
