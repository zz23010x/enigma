from django.db import models

# Create your models here.
class User(models.Model):
    account = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    authority = models.IntegerField()