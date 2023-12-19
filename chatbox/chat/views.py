import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Users, Conversation, Messages

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name and email:
            user, created = Users.objects.get_or_create(email=email, defaults={'name': name})
            return redirect('message_list', conversation_id=user.id)

    return render(request, 'chat/home.html')

def user_list(request):
    users = Users.objects.all()
    return render(request, 'chat/user_list.html', {'users': users})

def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})

def message_list(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)
    messages = Messages.objects.filter(conversation=conversation)

    if request.method == 'POST':
        time.sleep(1)  
        user_name = request.POST.get('name', '')
        user_email = request.POST.get('email', '')
        text = request.POST.get('message', '')

        if user_name and user_email and text:
            user, created = Users.objects.get_or_create(email=user_email, defaults={'name': user_name})
            Messages.objects.create(user=user, conversation=conversation, text=text)
            bot_user = Users.objects.get(name="d1")
            auto_reply = "Sending Message, please wait"
            Messages.objects.create(user=bot_user, conversation=conversation, text=auto_reply)

        return redirect('message_list', conversation_id=conversation_id)

    return render(request, 'chat/message_list.html', {'messages': messages, 'conversation': conversation})

def join_conversation(request):
    if request.method == 'POST':
        user_name = request.POST.get('name', '')
        user_email = request.POST.get('email', '')

        if user_name and user_email:
            user, created = Users.objects.get_or_create(email=user_email, defaults={'name': user_name})
            conversation = Conversation.objects.create()
            conversation.users.add(user)

            return redirect('message_list', conversation_id=conversation.id)

    return render(request, 'chat/home.html')
        


def view_messages(request, conversation_id):
    try:
        conversation = Conversation.objects.get(pk=conversation_id)
        messages = Messages.objects.filter(conversation=conversation)
    except Conversation.DoesNotExist:
        return render(request, 'chat/conversation_not_found.html')

    return render(request, 'chat/view_messages.html', {'conversation': conversation, 'messages': messages})