from django.db import models # type: ignore
from datetime import datetime

class User(models.Model):
    mail=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    type=models.CharField(type="guest")

class Payment(models.Model):
    mail=models.CharField(max_length=50)
    price=models.FloatField()
    date=models.DateField(date=datetime.today().strftime('%Y-%m-%d'))