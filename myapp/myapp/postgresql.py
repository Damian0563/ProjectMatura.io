import psycopg2
import bcrypt#type: ignore
from .models import User

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
        user.type = "admin"  # or any status you want
        user.save()
        return True
    except User.DoesNotExist:
        return False