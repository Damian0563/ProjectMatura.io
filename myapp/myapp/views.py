from django.shortcuts import render,redirect # type: ignore
import json
from django.urls import reverse #type:ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import ensure_csrf_cookie # type: ignore
from .models import User,Payment
from . import postgresql
from . import mail

def home(req):
    if(req.method=="GET"):
        return render(req,'myapp/home.html')
    
@ensure_csrf_cookie
def signUP(req):
    if req.method=="GET":
        return render(req,'myapp/signUP.html')
    elif req.method=="POST":
        data = json.loads(req.body)
        user_mail = data.get('mail')
        password = data.get('password')
        if(not postgresql.find(user_mail)):
            postgresql.insert(user_mail,password)
            mail.account_creation(user_mail)
            return JsonResponse({'status':200})
        else:
            return JsonResponse({'status':402})

@ensure_csrf_cookie
def signIN(req):
    if req.method=="GET":
        return render(req,'myapp/signIN.html')
    elif req.method=="POST":
        data=json.loads(req.body)
        mail=data.get('mail')
        password=data.get('password')
        remember_me_checked=data.get('remember',False)
        if(postgresql.check_credentials(mail,password)):
            id=postgresql.encode_id(mail)
            req.session['id']=id
            response = redirect('main')
            if remember_me_checked:
                token = postgresql.add_token(mail)
                response.set_cookie(
                    'remember_token',
                    token,
                    max_age=3600*24*30,
                    httponly=True,
                    secure=True 
                )
            return JsonResponse({'status':200,'redirect_url': reverse('main')})
        else:
            return JsonResponse({'status':404})
        
def main(req):
    if 'id' in req.session:
        mail = postgresql.decode_id(req.session['id'])    
    elif 'remember_token' in req.COOKIES:
        token = req.COOKIES['remember_token']
        mail = postgresql.get_mail_from_token(token)
        if mail:
            req.session['id'] = postgresql.encode_id(mail)
        else:
            return redirect('home') 
    else:
        return redirect('home')
    status = postgresql.get_status(mail)
    if status == "":
        return redirect('home')
    elif status == 'guest':
        return render(req, 'myapp/guest.html')
    else:
        return render(req, 'myapp/full.html')

    

def acc(req):
    return render(req,'myapp/account.html')