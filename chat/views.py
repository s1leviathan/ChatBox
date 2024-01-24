import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Conversation, Messages
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import openai
from django.conf import settings
from rest_framework import viewsets
from .serializers import ConversationSerializer, MessagesSerializer, UserSerializer



@login_required
def home(request):
    if request.method == 'POST':
        username = request.POST.get('name', '') 
        email = request.POST.get('email', '')

        if username and email:
            user, created = User.objects.get_or_create(email=email, defaults={'username': username})
            return redirect('message_list', conversation_id=user.id)

    return render(request, 'chat/home.html')

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'chat/user_list.html', {'users': users})

@login_required
def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})

@login_required
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
        openai_response = get_openai_response(text)
       
        bot_user, _ = User.objects.get_or_create(username='bot_user', defaults={'email': 'bot@example.com'})
        # import time
        # time.sleep(1)

        
        Messages.objects.create(user=bot_user, conversation=conversation, text=openai_response)
        

       
        messages = Messages.objects.filter(conversation=conversation)

    return render(request, 'chat/message_list.html', {'messages': messages, 'conversation': conversation})

@login_required
def join_conversation(request):
    if request.method == 'POST':
        user_name = request.POST.get('name', '')
        user_email = request.POST.get('email', '')

        if user_name and user_email:
            user, created = User.objects.get_or_create(email=user_email, defaults={'username': user_name})
            conversation = Conversation.objects.create()
            conversation.users.add(User)

            return redirect('message_list', conversation_id=conversation.id)

    return render(request, 'chat/home.html')
        

@login_required
def view_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    messages = Messages.objects.filter(conversation=conversation)

    return render(request, 'chat/view_messages.html', {'conversation': conversation, 'messages': messages})


def conversation_not_found(request):
    return render(request, 'chat/conversation_not_found.html')


def get_openai_response(prompt):
    openai.api_key = settings.OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request."

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer