from django.shortcuts import render, redirect
from .models import Users, Conversation, Messages

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name and email:
            user, created = Users.objects.get_or_create(email=email, defaults={'name': name})
            return redirect('user_conversations', user_id=user.id)

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
    return render(request, 'chat/message_list.html', {'messages': messages, 'conversation': conversation})