from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as log, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from .models import Chat, Message, Department, Users, Driver
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
    # Driver.objects.create(name='driver1', id = -983547137)
    # Users.objects.create(id=2, name='TIMA', password='1234', email='tima@gmail.com', isManager=False, tgid=626712893, department=Department.objects.get(id=12))
    # Chat.objects.create(driver=Driver.objects.get(id=-983547137), chat_name='test100', department=Department.objects.get(id=Users.objects.get(id=user).department.id), user=Users.objects.get(id=user))
    print(user)
    return render(request, 'chats/index.html', {'chats':Chat.objects.get(user=Users.objects.get(id=user)), 'me':user, })

def enter_chat(request):
    messages = Message.objects.filter(chat=request.GET.get('id')).all()
    # print(messages)

    return JsonResponse(data={'messages':serializers.serialize('json', messages)})