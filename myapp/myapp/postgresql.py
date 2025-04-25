import bcrypt#type: ignore
import time
from uuid import uuid4
from .models import User, Token, Payment

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

def check_waranty(mail):
    try:
        token=Token.objects.get(mail=mail)
        if token.waranty>=time.time():
            return True
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