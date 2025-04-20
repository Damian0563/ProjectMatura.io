from django.shortcuts import render
from django.http import HttpResponse

def home(req):
    if(req.method=="GET"):
        return render(req,'myapp/home.html')
    
def signUP(req):
    return render(req,'myapp/signUP.html')

def signIN(req):
    return render(req,'myapp/signIN.html')