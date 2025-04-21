from django.db import models

# Create your models here.
class Usuario(models.Model):
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50)


