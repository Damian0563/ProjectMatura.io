import bcrypt#type: ignore
import time
from uuid import uuid4
from .models import User, Token, Payment, UserProgress
import stripe
import os
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET')


def is_subscription_active(mail):
    try:
        payment = Payment.objects.get(mail=mail)
        if payment.stripe_subscription_id:
            subscription = stripe.Subscription.retrieve(payment.stripe_subscription_id)
            return subscription['status'] in ['active', 'trialing']
        return False
    except Payment.DoesNotExist:
        return False
    except Exception as e:
        print(f"Stripe error: {e}")
        return False

def get_subscription_id(mail):
    return Payment.objects.get(mail=mail).stripe_subscription_id
    
def delete_payment(mail):
    payment=Payment.objects.get(mail=mail)
    payment.delete()
    return

def insert_payment(mail, stripe_customer_id, stripe_subscription_id):
    try:
        payment = Payment.objects.get(mail=mail)
        payment.stripe_customer_id = stripe_customer_id
        payment.stripe_subscription_id = stripe_subscription_id
        payment.save()
    except Payment.DoesNotExist:
        Payment.objects.create(mail=mail, stripe_customer_id=stripe_customer_id, stripe_subscription_id=stripe_subscription_id)

def find(mail):
    return User.objects.filter(mail=mail).exists()
        
def insert(mail, password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    User.objects.create(mail=mail, password=hashed.decode('utf-8'), type="guest")

def check_credentials(mail, password):
    try:
        user = User.objects.get(mail=mail)
    except User.DoesNotExist:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

def change_status(mail):
    try:
        user = User.objects.get(mail=mail)
        user.type = "admin"
        user.save()
        return True
    except User.DoesNotExist:
        return False
    
shift=4
def encode_id(mail):
    result=''
    for i in range(len(mail)):
        if chr(ord(mail[i])+shift):
            result+=chr(ord(mail[i])+shift)
    return result

def decode_id(id):
    result=''
    for i in range(len(id)):
        if(chr(ord(id[i])-shift)):
            result+=str(chr(ord(id[i])-shift))
    return result


def get_progress(mail):
    try:
        return [progress.courses for progress in UserProgress.objects.filter(mail=mail)]
    except UserProgress.DoesNotExist:
        return None

def save_course(mail,course):
    try:
        past=UserProgress.objects.get(mail=mail,courses=course)
        past.delete()
    except UserProgress.DoesNotExist:
        pass
    UserProgress.objects.create(mail=mail,courses=course)
    return

def get_status(mail):
    try:
        user = User.objects.get(mail=mail)
        return user.type
    except User.DoesNotExist:
        return ""
    
def add_token(mail):
    token=str(uuid4())
    waranty=time.time()+3600*24*30
    Token.objects.create(mail=mail,token=token,waranty=waranty)
    return token

def delete_tokens(mail):
    try:
        tokens = Token.objects.filter(mail=mail)
        tokens.delete()
    except Token.DoesNotExist:
        pass

def check_waranty(mail):
    try:
        token=Token.objects.get(mail=mail)
        if token.waranty>=time.time():
            return True
        delete_tokens(mail)
        return False
    except Token.DoesNotExist:
        return False
    
def get_mail_from_token(token_value):
    try:
        token = Token.objects.get(token=token_value)
        if token.waranty >= time.time():
            return token.mail
    except Token.DoesNotExist:
        pass
    return None