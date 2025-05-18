from django.db import models # type: ignore

class User(models.Model):
    mail=models.CharField(max_length=50)
    password=models.CharField(max_length=60)
    type=models.CharField(max_length=10)

class Payment(models.Model):
    mail=models.CharField(max_length=50)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

class Token(models.Model):
    mail=models.CharField(max_length=50)
    token=models.CharField(max_length=100)
    waranty=models.FloatField()

class UserProgress(models.Model):
    mail=models.CharField(max_length=50)
    courses=models.CharField(max_length=30)

class UserAuth(models.Model):
    mail=models.CharField(max_length=50)
    code=models.CharField(max_length=10)