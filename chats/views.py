from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as log, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from .models import Chat, Message, Department, Users
from django.db.models import Q
from django.core import serializers

# Create your views here.
def index(request, user):
    # Message.objects.all().delete()
    # Chat.objects.all().delete()
    # Department.objects.all().delete()
    # Users.objects.all().delete()
    # Department.objects.create(name='sale')
    # Department.objects.create(name='document')
    # chat = Chat.objects.create(id=-814587432, chat_name='driver3')
    # chat = Chat.objects.get(id=-919418148)
    # chat.users.add(Users.objects.get(id=141))
    # chat.users.add(Users.objects.get(id=142))
    # chat.users.add(Users.objects.get(id=29))
    # chat = Chat.objects.get(id=-819593283)
    # chat.users.add(Users.objects.get(id=23))
    # chat.users.add(Users.objects.get(id=141))
    # chat.users.add(Users.objects.get(id=142))
    # chat.users.add(Users.objects.get(id=29))

    # user = Users.objects.get(id=23)
    # user.tgid = 954130482
    # user.save()


    print(user)
    return render(request, 'chats/index.html', {'chats':Chat.objects.filter(users=Users.objects.get(id=user)), 'me':user, 'chats_ser':serializers.serialize('json', Chat.objects.filter(users=Users.objects.get(id=user))), 'department':Users.objects.get(id=user).department.name})

def enter_chat(request):
    messages = Message.objects.filter(chat=request.GET.get('id')).all()

    return JsonResponse(data={'messages':serializers.serialize('json', messages)})