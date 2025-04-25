from django.db import models # type: ignore

class User(models.Model):
    mail=models.CharField(max_length=50)
    password=models.CharField(max_length=60)
    type=models.CharField(max_length=10)

class Payment(models.Model):
    mail=models.CharField(max_length=50)
    price=models.FloatField()
    date=models.DateField()

class Token(models.Model):
    mail=models.CharField(max_length=50)
    token=models.CharField(max_length=100)
    waranty=models.FloatField()