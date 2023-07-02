from django.http import JsonResponse
from .models import Chat, Message, Users
from django.core import serializers
from time import time
import asyncio
from django.shortcuts import render
from .db_manager import DBManager
from . import bot_documents, bot_sales, bot_trucks
from .bots import BOTS

# Create your views here.
def index(request, user):
    return render(request, 'chats/android.html', {'chats':Chat.objects.filter(users=Users.objects.get(id=user)), 'me':user, 'chats_ser':serializers.serialize('json', Chat.objects.filter(users=Users.objects.get(id=user))), 'department':Users.objects.get(id=user).department.name})

def enter_chat(request):
    messages = list(Message.objects.filter(chat=request.GET.get('id')).all())[-30:]
    return JsonResponse(data={'messages':serializers.serialize('json', messages)})

def get_update(request):
    chat = int(request.GET.get('id'))
    old_time = int(request.GET.get('old'))
    cur_time = int(time())
    messages = Message.objects.filter(chat=chat).filter(time__gte=old_time).filter(time__lt=cur_time).all()
    return JsonResponse(data={'old':cur_time, 'messages':serializers.serialize('json', messages)})

def send_message(request):
    chat=int(request.GET.get('chat'))
    user=int(request.GET.get('user'))
    message=request.GET.get('message')
    department=request.GET.get('department')
    try:
        if str(user) == "60":
            tgid = asyncio.run(BOTS["Truck"].send_message(chat, message))
            db = DBManager()
            db.insert_message(tgid, user, message, chat, department, 'text')
        else:
            tgid = asyncio.run(BOTS[department].send_message(chat, message))
            db = DBManager()
            db.insert_message(tgid, user, message, chat, department, 'text')
    except:
        return JsonResponse(data={'response':False})
    return JsonResponse(data={'response':True})



def get_old(request):
    count = int(request.GET.get('count'))
    print(count)
    messages = list(Message.objects.filter(chat=request.GET.get('id')).all())[-30*(count+1):-30*(count)]
    return JsonResponse(data={'messages':serializers.serialize('json', messages)})

def index_chat(request, user, chat):
    return render(request, 'chats/index_chat.html', {'chat':chat, 'me':user, 'chats_ser':serializers.serialize('json', Chat.objects.filter(users=Users.objects.get(id=user))), 'department':Users.objects.get(id=user).department.name})