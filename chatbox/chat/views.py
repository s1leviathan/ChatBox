from django.shortcuts import render, redirect
from .models import Users, Conversation, Messages

def user_list(request):
    users = Users.objects.all()
    return render(request, 'chat/user_list.html', {'users': users})

def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})