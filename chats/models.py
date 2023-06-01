from django.db import models
from time import time

# Create your models here.
class Driver(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=64)

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)

class Users(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    tgid = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    isManager = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    chat_name = models.CharField(max_length=128, unique=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    tgid = models.IntegerField(null=True)
    from_user = models.CharField(max_length=64)
    # time = models.TimeField(default=time())
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(null=True)

class Issue(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    priority = models.IntegerField()
    responsiblePerson = models.ForeignKey(Users, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=64)
    startTime = models.DateTimeField(max_length=64)
    time = models.TimeField()
    endTime = models.DateTimeField()
    department = models.CharField(max_length=64)