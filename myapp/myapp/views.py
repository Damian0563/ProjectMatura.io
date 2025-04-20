from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


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
        return JsonResponse({'status':'success'})

@ensure_csrf_cookie
def signIN(req):
    if req.method=="GET":
        return render(req,'myapp/signIN.html')
    elif req.method=="POST":
        data=json.loads(req.body)
        mail=data.get('mail')
        password=data.get('password')
        return JsonResponse({'status':'success'})