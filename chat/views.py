import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Conversation, Messages
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name and email:
            user, created = User.objects.get_or_create(email=email, defaults={'name': name})
            return redirect('message_list', conversation_id=user.id)

    return render(request, 'chat/home.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'chat/user_list.html', {'users': users})

def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})

def message_list(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)
    messages = Messages.objects.filter(conversation=conversation)
    user= request.user

    if request.method == 'POST':
        text = request.POST.get('message', '')

       
       
       
        # user_name = request.session.get('name', 'DefaultName')
        # user_email = request.session.get('email')
        # print(user_name, '+' , user_email)
        # user, created = User.objects.get_or_create(email=user_email, defaults={'name': user_name})

     
        Messages.objects.create(user=user, conversation=conversation, text=text)

       
        # import time
        # time.sleep(1)

        bot_user_name = 'dimitris'
        bot_user, _ = User.objects.get_or_create(name=bot_user_name, defaults={'email': 'd.zourdoumis@gmail.com'})

       
        if user != bot_user:
            auto_reply = "Sorry"
            Messages.objects.create(user=bot_user, conversation=conversation, text=auto_reply)

       
        messages = Messages.objects.filter(conversation=conversation)

    return render(request, 'chat/message_list.html', {'messages': messages, 'conversation': conversation})

def join_conversation(request):
    if request.method == 'POST':
        user_name = request.POST.get('name', '')
        user_email = request.POST.get('email', '')

        if user_name and user_email:
            user, created = User.objects.get_or_create(email=user_email, defaults={'name': user_name})
            conversation = Conversation.objects.create()
            conversation.users.add(user)

            return redirect('message_list', conversation_id=conversation.id)

    return render(request, 'chat/home.html')
        


def view_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    messages = Messages.objects.filter(conversation=conversation)

    return render(request, 'chat/view_messages.html', {'conversation': conversation, 'messages': messages})


def conversation_not_found(request):
    return render(request, 'chat/conversation_not_found.html')