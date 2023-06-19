from django.db import models
from time import time

# Create your models here.
# class Driver(models.Model):
#     id = models.CharField(primary_key=True, max_length=64)
#     name = models.CharField(max_length=64)

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
    id = models.IntegerField(primary_key=True)
    chat_name = models.CharField(max_length=128, null=True)
    users = models.ManyToManyField(Users)
    
class Message(models.Model):
    PHOTO = "photo"
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    TYPE_OF_MESSAGE_CHOICES=[
        (PHOTO, "photo"),
        (TEXT, "text"),
        (AUDIO, "audio"),
        (VIDEO, "video")
    ]

    id = models.AutoField(primary_key=True)
    tgid = models.IntegerField(null=True)
    from_user = models.CharField(max_length=64)
    departmentName = models.CharField(max_length=64, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    typeOfMessage = models.CharField(max_length=25, choices=TYPE_OF_MESSAGE_CHOICES, default=TEXT)

class Issue(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    priority = models.IntegerField()
    responsiblePerson = models.ForeignKey(Users, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=64)
    # startTime = models.DateTimeField(max_length=64)
    # time = models.TimeField(default=111)
    # endTime = models.DateTimeField(time())
    department = models.CharField(max_length=64)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)