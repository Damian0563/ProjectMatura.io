from django.shortcuts import render,redirect # type: ignore
import json
from django.urls import reverse #type:ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt # type: ignore
from . import postgresql
from django.http import HttpResponse # type: ignore
from . import mail
from uuid import uuid4 # type: ignore
import os
import stripe
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET')
def home(req):
    if(req.method=="GET"):
        if 'id' in req.session:
            return redirect('main')
        if os.getenv("TOKEN") in req.COOKIES and req.COOKIES[os.getenv("TOKEN")]!=None:
            token = req.COOKIES[os.getenv("TOKEN")]
            mail = postgresql.get_mail_from_token(token)
            if mail:
                req.session['id'] = postgresql.encode_id(mail)
                return redirect('main')
        return render(req,'myapp/home.html')
    
def expired(req):
    return render(req,'myapp/session_expired.html')


@ensure_csrf_cookie
def check(req):
    data = json.loads(req.body)
    user_mail = data.get('mail')
    if postgresql.find(user_mail):      
        return JsonResponse({'message': 'User already exists','code':400})
    else:
        mail.account_creation(user_mail)
        return JsonResponse({'message': 'Success','code':200})
        

@ensure_csrf_cookie
def signUP(req):
    if req.method=="GET":
        if 'id' in req.session: return redirect('main')
        if os.getenv('TOKEN') in req.COOKIES and req.COOKIES[os.getenv('TOKEN')]!=None:
            token = req.COOKIES[os.getenv('TOKEN')]
            email = postgresql.get_mail_from_token(token)
            if email:
                req.session['id'] = postgresql.encode_id(email)
                return redirect('main')
        return render(req,'myapp/signUP.html')
    elif req.method=="POST":
        data = json.loads(req.body)
        user_mail = data.get('mail')
        password = data.get('password')
        code=data.get('code')
        if(code==postgresql.get_auth(user_mail)):
            postgresql.insert(user_mail,password)
            req.session['id'] = postgresql.encode_id(user_mail)
            return JsonResponse({'code':'good'})
        return JsonResponse({'code':'bad'})

@ensure_csrf_cookie
def restore(req,id):
    email=postgresql.decode_id(id)
    if req.method=='GET':
        return render(req,'myapp/restore.html',{'mail':email})
    elif req.method=='PUT':
        data=json.loads(req.body)
        new_password=data.get('new_password')
        if postgresql.change_password(email,new_password):
            return JsonResponse({'status':200})
        return JsonResponse({'status':500})

@ensure_csrf_cookie
def encode(req):
    data = json.loads(req.body)
    user_mail = data.get('mail')
    if postgresql.find(user_mail):
        encoding=postgresql.encode_id(user_mail)
        return JsonResponse({'status':200,'url':f"/restore/{encoding}"})
    return JsonResponse({'status':400})

@ensure_csrf_cookie
def signIN(req):
    if req.method=="GET":
        if 'id' in req.session: redirect('main')
        if os.getenv("TOKEN") in req.COOKIES and req.COOKIES[os.getenv('TOKEN')]!=None:
            token = req.COOKIES[os.getenv('TOKEN')]
            mail = postgresql.get_mail_from_token(token)
            if mail:
                req.session['id'] = postgresql.encode_id(mail)
                return redirect('main')
        return render(req,'myapp/signIN.html')
    elif req.method=="POST":
        mail=req.POST.get('mail')
        password=req.POST.get('password')
        remember_me_checked=req.POST.get('remember')
        if(postgresql.check_credentials(mail,password)):
            id=postgresql.encode_id(mail)
            req.session['id']=id
            response = redirect('main')
            if remember_me_checked!=None:
                postgresql.delete_tokens(mail)
                token = postgresql.add_token(mail)
                response.set_cookie(
                    os.getenv("TOKEN"),
                    token,
                    max_age=3600*24*30,
                    httponly=True,
                    secure=True 
                )
            return response
        else:
            return render(req,'myapp/signIN.html',{'error':True})
        
def main(req):
    if 'id' in req.session:
        mail = postgresql.decode_id(req.session['id'])  
        if mail is None: return redirect('expired')
    elif os.getenv('TOKEN') in req.COOKIES:
        token = req.COOKIES[os.getenv('TOKEN')]
        mail = postgresql.get_mail_from_token(token)
        if mail:
            req.session['id'] = postgresql.encode_id(mail)
        else: return redirect('expired')    
    if postgresql.is_subscription_active(mail):
        courses=postgresql.get_progress(mail)
        if courses!=None:
            return render(req, 'myapp/full.html',{'mail': mail,'courses':courses})
        return render(req, 'myapp/full.html',{'mail': mail})
    else:
        return render(req, 'myapp/guest.html',{'mail': mail})
    
        
    
def log_out(req):
    if req.method=='POST':
        req.session.flush() 
        remember_token = req.COOKIES.get(os.getenv('TOKEN'))
        if remember_token!=None:
            postgresql.delete_tokens(remember_token)
        response = redirect('signIN')
        response.delete_cookie(os.getenv('TOKEN'))
        return response


def acc(req):
    if req.method=="GET":
        if 'id' in req.session:
            mail=postgresql.decode_id(req.session.get('id'))
            if postgresql.find(mail):
                type=True
                if postgresql.is_subscription_active(mail):
                    progress=round(len(postgresql.get_progress(mail))*100/14)
                    type=False
                    return render(req,'myapp/account.html',{'mail': mail,'type':type,'progress':progress})
                return render(req,'myapp/account.html',{'mail': mail,'type':type,'progress':0})
        else:
            token = req.COOKIES[os.getenv('TOKEN')]
            if token!=None:
                mail=postgresql.get_mail_from_token(token)
                if postgresql.find(mail):
                    type=True
                    if postgresql.is_subscription_active(mail): type=False
                    return render(req,'myapp/account.html',{'mail': mail,'type':type})
        return redirect('expired')

def success(req):
    return render(req,'myapp/success.html')

@ensure_csrf_cookie
def create_checkout_session(req):
    data=json.loads(req.body)
    checkout_session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/fail',
        customer_email=data["mail"],
        line_items=[{
            "price": data["priceId"],
            "quantity": 1,
        }],
    )
    return JsonResponse({'sessionId':checkout_session.id})

@ensure_csrf_cookie
def resign(req):
    if req.method=='POST':
        email=postgresql.decode_id(req.session['id'])
        sub_id=postgresql.get_subscription_id(email)
        if sub_id!=None:
            stripe.Subscription.delete(sub_id)
            mail.cancelation(email)
            postgresql.delete_payment(email)
        return redirect('home')


@csrf_exempt
def stripe_webhook(req):
    payload = req.body
    sig_header = req.headers.get('stripe-signature')
    endpoint_secret = os.getenv('ENDPOINT_SECRET')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_id = session.get('customer')
        if not customer_id:
            return JsonResponse({'status': 400})
        subscription_id = session.get('subscription')
        customer = stripe.Customer.retrieve(customer_id)
        customer_email = customer['email']
        postgresql.insert_payment(customer_email, customer_id, subscription_id)
        mail.payment(customer_email)
    return JsonResponse({'status': 200})

def fail(req):
    return render(req,'myapp/fail.html')

@ensure_csrf_cookie
def progress(req):
    data = json.loads(req.body)
    course = data.get('course')
    if 'id' in req.session:
        mail=postgresql.decode_id(req.session.get('id'))
        if(postgresql.find(mail)):
            postgresql.save_course(mail,course)
            return JsonResponse({'status':200})
    elif req.COOKIES[os.getenv('TOKEN')]!=None:
        mail=postgresql.get_mail_from_token(req.COOKIES[os.getenv('TOKEN')])
        if(postgresql.find(mail)):
            postgresql.save_course(mail,course)
            return JsonResponse({'status':200})
    return JsonResponse({'status':404})

def get_progress(req):
    if 'id' in req.session:
        mail=postgresql.decode_id(req.session.get('id'))
        
        if(postgresql.find(mail)): 
            content=postgresql.get_progress(mail)
            if content!=None:
                return JsonResponse({'status':200,'courses':postgresql.get_progress(mail)})
            return JsonResponse({'status':200})
    elif req.COOKIES[os.getenv('TOKEN')]!=None:
        mail=postgresql.get_mail_from_token(req.COOKIES[os.getenv('TOKEN')])
        if(postgresql.find(mail)): 
            content=postgresql.get_progress(mail)
            if content!=None:
                return JsonResponse({'status':200,'courses':postgresql.get_progress(mail)})
            return JsonResponse({'status':200})
    return JsonResponse({'status':404})