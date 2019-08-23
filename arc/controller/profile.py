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
    pic=''
    if display_picture.objects.filter(idx = request.user.id).exists()==True:
        pic = display_picture.objects.get(idx = request.user.id)
    else:
        pass
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

        if 'image_upload' in request.POST:
            image = request.FILES['file1']
            if display_picture.objects.filter(idx=request.user.id).exists():
                z = display_picture.objects.get(idx=request.user.id)
                z.profile_picture = image
                z.save()
            else:
                z = display_picture(idx=request.user.id,profile_picture=image)
                z.save()
            return redirect('profile')

    return render(request,'profile.html/',{'pic':pic,'name':name,'info1':info1,'info':info,'check':check,'var':var})
