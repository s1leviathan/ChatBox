from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Messages


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ConversationSerializer(serializers.ModelSerializer):
    User = UserSerializer(many=True, read_only=True)  

    class Meta:
        model = Conversation
        fields = ['id', 'User', 'date']


class MessagesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  
    conversation = ConversationSerializer(read_only=True)  

    class Meta:
        model = Messages
        fields = ['id', 'user', 'conversation', 'text', 'date']
