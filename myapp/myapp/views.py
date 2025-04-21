from django.shortcuts import render # type: ignore
import json
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import ensure_csrf_cookie # type: ignore
from .models import User,Payment
from . import postgresql

def home(req):
    if(req.method=="GET"):
        return render(req,'myapp/home.html')
    
@ensure_csrf_cookie
def signUP(req):
    if req.method=="GET":
        return render(req,'myapp/signUP.html')
    elif req.method=="POST":
        data = json.loads(req.body)
        mail = data.get('mail')
        password = data.get('password')
        if(not postgresql.find(mail)):
            postgresql.insert(mail,password)
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
        if(postgresql.check_credentials(mail,password)):
            id=postgresql.encode_id(mail)
            return JsonResponse({'status':200,'id':id})
        else:
            return JsonResponse({'status':402})
        

def main(req,id):
    req.session['test']='hello'
    return render(req,'myapp/main.html')